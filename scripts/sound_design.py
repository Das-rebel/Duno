#!/usr/bin/env python3
"""Duno R2 — sound-design stage.
Procedural CC0 SFX (no downloads, no licensing) + music sidechain-duck under VO.

usage: sound_design.py --vo vo.mp3 --music music.mp3 --beats beats.json \
         --video-len 67.86 --out mixed.m4a [--sfx-vol 0.5] [--music-vol 0.12]
beats.json: [{"t": 3.2, "sfx": "impact"}, {"t": 14.0, "sfx": "whoosh"}, ...]
"""
import argparse, json, subprocess, tempfile, os, sys
import numpy as np
from scipy.io import wavfile as wf

SR = 44100

def impact(dur=0.6):
    n = int(SR * dur); t = np.linspace(0, dur, n)
    thump = np.sin(2 * np.pi * (110 * np.exp(-t * 6)) * t) * np.exp(-t * 9)
    noise = np.random.default_rng(7).standard_normal(n) * np.exp(-t * 22)
    noise = np.convolve(noise, np.ones(24) / 24, mode="same")  # lowpass-ish
    s = thump * 0.9 + noise * 0.5
    return (s / np.max(np.abs(s)) * 0.9)

def whoosh(dur=0.45):
    n = int(SR * dur); t = np.linspace(0, dur, n)
    env = np.sin(np.pi * t / dur) ** 2
    noise = np.random.default_rng(3).standard_normal(n)
    # moving bandpass feel: modulate with swept sine
    sweep = np.sin(2 * np.pi * (300 + 1400 * t / dur) * t)
    s = (noise * 0.35 + sweep * 0.2) * env
    return (s / np.max(np.abs(s)) * 0.5)

def tick(dur=0.05):
    n = int(SR * dur); t = np.linspace(0, dur, n)
    s = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 120)
    return (s / np.max(np.abs(s)) * 0.4)

GEN = {"impact": impact, "whoosh": whoosh, "tick": tick}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vo", required=True); ap.add_argument("--music", required=True)
    ap.add_argument("--beats", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--video-len", type=float, required=True)
    ap.add_argument("--sfx-vol", type=float, default=0.5)
    ap.add_argument("--music-vol", type=float, default=0.12)
    a = ap.parse_args()

    beats = json.load(open(a.beats))
    tmp = tempfile.mkdtemp()
    inputs, filters, labels = [], [], []

    # pre-pad VO to full video length (sidechaincompress truncates at raw VO
    # EOF otherwise — verified ffmpeg 8.1 quirk)
    vo_pad = os.path.join(tmp, "vo_padded.wav")
    r0 = subprocess.run(["ffmpeg", "-y", "-i", a.vo, "-af",
        f"apad=whole_dur={a.video_len}", "-t", str(a.video_len), vo_pad],
        capture_output=True, text=True)
    if r0.returncode != 0:
        sys.exit(r0.stderr[-400:])
    a.vo = vo_pad

    # 0=vo(padded), 1=music; sfx files appended from index 2
    idx = 2
    for i, b in enumerate(beats):
        kind = b["sfx"]
        if kind not in GEN:
            sys.exit(f"unknown sfx '{kind}' (have: {list(GEN)})")
        f = os.path.join(tmp, f"sfx{i}.wav")
        wf.write(f, SR, (GEN[kind]() * 32767).astype(np.int16))
        inputs += ["-i", f]
        ms = int(b["t"] * 1000)
        filters.append(f"[{idx}:a]adelay={ms}|{ms}[s{i}]")
        labels.append(f"[s{i}]")
        idx += 1

    # duck music under VO: music(main) keyed by vo(sidechain)
    duck = (f"[1:a]volume={a.music_vol}[mus];"
            f"[mus][0:a]sidechaincompress=threshold=0.02:ratio=6:attack=80:release=420[mdk]")
    mix_ins = "[0:a][mdk]" + "".join(labels)
    n_in = 2 + len(beats)
    filters.append(duck)
    filters.append(f"{mix_ins}amix=inputs={n_in}:duration=first:dropout_transition=0,atrim=0:{a.video_len}[out]")
    fc = ";".join(filters)

    cmd = ["ffmpeg", "-y", "-i", a.vo, "-stream_loop", "-1", "-i", a.music] + inputs + \
          ["-filter_complex", fc, "-map", "[out]", "-c:a", "aac", "-b:a", "192k", a.out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-600:])
    print(f"✓ {a.out} — {len(beats)} SFX events, music ducked under VO")

if __name__ == "__main__":
    main()
