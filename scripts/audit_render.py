#!/usr/bin/env python3
"""Duno audit — extract frames at multiple VO timestamps for visual review.

The single highest-leverage 5 minutes before shipping any rendered video:
extract 15-20 frames at evenly-spaced timestamps across the composition,
view each one, and check that every key visual element is actually in-frame
at the moment the VO mentions it. This catches the bugs that source-code
review misses: off-canvas content (caused by `top:` offsets inside padded
parents), animations that fire too late, struck-through climax text that
never renders, waveform timelines rendered off-screen, captions that
drift out of sync across transition fades.

Usage:
  audit_render.py master.mp4                      # extract 16 frames, 1/8s apart
  audit_render.py master.mp4 --count 24          # 24 frames, evenly spaced
  audit_render.py master.mp4 --at 2,8,14,28     # at specific timestamps
  audit_render.py master.mp4 --beat-map beats.json  # at VO beat boundaries

Output: a frames/ directory with timestamped JPGs + a summary checklist.

The script itself can't see the frames — it extracts them so you can.
The discipline is opening each one and asking: "is the visual the VO is
describing actually on screen right now?"
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

def ffprobe_duration(video: str) -> float:
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0", video],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def ffprobe_fps(video: str) -> float:
    r = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
                        "-show_entries","stream=r_frame_rate","-of","csv=p=0", video],
                       capture_output=True, text=True)
    rate = r.stdout.strip().split("\n")[0].split(",")[0].strip()
    if "/" in rate:
        n, d = rate.split("/")
        try:
            return float(n) / float(d)
        except ValueError:
            return 30.0
    try:
        return float(rate)
    except ValueError:
        return 30.0

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", help="rendered mp4 to audit")
    ap.add_argument("--out", default="frames", help="output directory for JPG frames")
    ap.add_argument("--count", type=int, default=16, help="number of frames to extract (default 16)")
    ap.add_argument("--at", help="comma-separated specific timestamps in seconds")
    ap.add_argument("--beat-map", help="JSON file with VO beat boundaries {start, end, text}")
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(exist_ok=True)
    duration = ffprobe_duration(args.video)
    fps = ffprobe_fps(args.video)
    print(f"→ {args.video}  ({duration:.1f}s, {fps:.0f}fps)")

    if args.at:
        times = [float(t) for t in args.at.split(",")]
        reason = f"explicit timestamps ({len(times)} frames)"
    elif args.beat_map:
        beats = json.load(open(args.beat_map))
        # sample at the START of each beat (when the visual should appear)
        times = [b["start"] for b in beats if "start" in b]
        reason = f"VO beat boundaries ({len(times)} beats)"
    else:
        # Evenly-spaced — 16 samples across the duration
        n = args.count
        times = [duration * i / (n + 1) for i in range(1, n + 1)]
        reason = f"evenly spaced ({n} samples)"

    print(f"→ extracting {len(times)} frames ({reason}) into {out}/")
    for t in times:
        ts = max(0, min(t, duration - 0.05))
        fname = out / f"t_{ts:06.2f}s.jpg"
        r = subprocess.run(["ffmpeg","-y","-ss", f"{ts:.2f}", "-i", args.video,
                            "-vframes","1","-q:v","2","-loglevel","error", str(fname)],
                           capture_output=True)
        if r.returncode != 0:
            print(f"  ✗ {fname.name} failed: {r.stderr.decode()[:200]}")
    print(f"→ done. open {out}/t_*.jpg and audit each frame.")
    print("")
    print("CHECKLIST per frame:")
    print("  [ ] The visual the VO is describing is actually ON SCREEN")
    print("  [ ] No elements clipped off the canvas edges")
    print("  [ ] Animation completed or in mid-state (not stuck at spring start)")
    print("  [ ] Caption band matches the VO being spoken at this timestamp")
    print("  [ ] Top + bottom halves both have content (no top- or bottom-heavy gaps)")

if __name__ == "__main__":
    main()
