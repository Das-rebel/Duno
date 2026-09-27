#!/usr/bin/env python3
"""Duno R1 — machine-watched QA. `duno qa` stage.

usage: qa_video.py --video master.mp4 --beats qa_beats.json [--backend heuristic|vlm|marlin]
qa_beats.json: [{"name":"hook","start":0.0,"end":9.5,"expect":"$4,217 invoice number"}, ...]

heuristic (default, zero-dep): duration drift · motion detection (frame diffs at
10/50/90% of each beat) · audio energy per beat · tail-freeze check.
vlm: OpenAI-compatible endpoint via env VLM_BASE_URL/VLM_MODEL/VLM_API_KEY —
sends 3 frames per beat, asks for on-screen text/scene description, diffs vs `expect`.
marlin: HappyyPablo/Marlin-2B local VLM if importable.
Exit 0 iff no DRIFT.
"""
import argparse, json, os, subprocess, sys, tempfile, base64
import numpy as np
from PIL import Image

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def dur_of(f):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])
    return float(r.stdout.strip())

def extract(video, t, out):
    sh(["ffmpeg", "-y", "-ss", f"{max(t,0):.2f}", "-i", video, "-vframes", "1", "-vf", "scale=640:-2", out])

def frame_arr(p):
    return np.asarray(Image.open(p).convert("L"), dtype=np.float32)

def audio_rms_at(video, start, end, tmp):
    seg = os.path.join(tmp, "seg.wav")
    sh(["ffmpeg", "-y", "-ss", f"{start:.2f}", "-to", f"{end:.2f}", "-i", video,
        "-vn", "-ac", "1", "-ar", "16000", seg])
    r = sh(["ffmpeg", "-i", seg, "-af", "volumedetect", "-f", "null", "-"])
    for line in r.stderr.splitlines():
        if "mean_volume" in line:
            return float(line.split(":")[1].replace(" dB", "").strip())
    return -99.0

def vlm_describe(frames, base_url, model, key):
    import urllib.request
    content = [{"type": "text", "text": "Describe what is on screen. Quote any visible text exactly."}]
    for f in frames:
        b64 = base64.b64encode(open(f, "rb").read()).decode()
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps({"model": model, "messages": [{"role": "user", "content": content}]}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)["choices"][0]["message"]["content"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--beats", required=True)
    ap.add_argument("--backend", choices=["heuristic", "vlm", "marlin"], default="heuristic")
    ap.add_argument("--freeze-ok-sec", type=float, default=5.0, help="expected static tail (CTA dwell)")
    a = ap.parse_args()
    beats = json.load(open(a.beats))
    total = dur_of(a.video)
    tmp = tempfile.mkdtemp()
    results, drifts = [], 0

    for i, b in enumerate(beats):
        s, e = float(b["start"]), float(b["end"])
        notes, status = [], "PASS"

        # 1. drift vs timeline
        if i < len(beats) - 1 and abs(beats[i+1]["start"] - e) > 1.0:
            notes.append(f"gap to next beat {beats[i+1]['start']-e:+.2f}s (boundary not adjacent)")

        # 2. motion detection
        f1, f2, f3 = (os.path.join(tmp, f"b{i}_1.jpg"), os.path.join(tmp, f"b{i}_2.jpg"), os.path.join(tmp, f"b{i}_3.jpg"))
        extract(a.video, s + (e-s)*0.10, f1); extract(a.video, s + (e-s)*0.50, f2); extract(a.video, s + (e-s)*0.90, f3)
        d12 = float(np.mean(np.abs(frame_arr(f2) - frame_arr(f1))))
        d23 = float(np.mean(np.abs(frame_arr(f3) - frame_arr(f2))))
        motion = d12 + d23
        if motion < 4.0 and (total - e) > a.freeze_ok_sec:
            notes.append(f"low motion ({motion:.1f}) — possible static frame regression")
            status = "DRIFT"

        # 3. audio energy
        rms = audio_rms_at(a.video, s, e, tmp)
        if rms < -45 and e < total - a.freeze_ok_sec:
            notes.append(f"silent beat ({rms:.0f} dB)")
            status = "WARN"

        # 4. VLM text/scene check (optional backends)
        if a.backend in ("vlm", "marlin") and b.get("expect"):
            desc = ""
            if a.backend == "vlm":
                desc = vlm_describe([f2], os.environ["VLM_BASE_URL"], os.environ["VLM_MODEL"],
                                    os.environ.get("VLM_API_KEY", "sk-noop"))
            elif a.backend == "marlin":
                try:
                    from marlin import Marlin  # type: ignore
                    desc = Marlin().describe(a.video, s, e)  # model API: happening + spoken
                except Exception as ex:
                    notes.append(f"marlin unavailable ({type(ex).__name__}) — install per ROADMAP R1")
            hit = any(w.lower() in desc.lower() for w in b["expect"].split())
            if desc and not hit:
                notes.append(f"expected '{b['expect']}' not confirmed — VLM said: {desc[:80]!r}")
                status = "DRIFT"
            elif desc:
                notes.append(f"vlm: {desc[:60]!r}")

        if status == "DRIFT": drifts += 1
        results.append((b["name"], status, motion, rms, "; ".join(notes) or "ok"))

    # 5. tail freeze (expected)
    tl, te = os.path.join(tmp, "t1.jpg"), os.path.join(tmp, "t2.jpg")
    # sample two PRE-FADE points so the intentional end-fade isn't flagged as motion
    extract(a.video, total - a.freeze_ok_sec - 0.5, tl); extract(a.video, total - 1.6, te)
    tfreeze = float(np.mean(np.abs(frame_arr(te) - frame_arr(tl))))
    tail_status = "PASS" if tfreeze < 12 else "WARN"
    results.append(("tail-dwell", tail_status, tfreeze, 0, "static as designed" if tfreeze < 12 else "tail not static"))

    w = max(len(r[0]) for r in results)
    print("═" * 78)
    print(f"  DUNO QA — {os.path.basename(a.video)}  ({total:.1f}s, backend={a.backend})")
    print("═" * 78)
    for name, st, mo, rm, note in results:
        mark = {"PASS": "✅", "WARN": "⚠️ ", "DRIFT": "❌"}[st]
        print(f"  {mark} {name:<{w}}  motion={mo:6.1f}  rms={rm:6.0f}dB  {note}")
    print("─" * 78)
    verdict = "PASS" if drifts == 0 else f"FAIL ({drifts} drift)"
    print(f"  VERDICT: {verdict}")
    print("═" * 78)
    sys.exit(0 if drifts == 0 else 1)

if __name__ == "__main__":
    main()
