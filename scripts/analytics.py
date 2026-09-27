#!/usr/bin/env python3
"""Duno R3 — closed-loop hook analytics.
Parses a YouTube Studio "Reach > Viewer retention" CSV export (or any CSV with
video id/name + retention % columns) and names the winning hook variant.

usage: analytics.py retention.csv [--at-sec 30]
Expected CSV columns (YouTube export): "Video title","Video ID",...,and one or
more "Percentages watched at X seconds" style columns — OR a simple form:
  variant,retention_30s   (one row per variant)

The loop: render_variants.sh → upload all → wait 48h → export CSV → analytics.py
→ winning variant becomes defaultProps in Root.tsx.
"""
import argparse, csv, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--at-sec", type=int, default=30)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.csv_path)))
    if not rows:
        sys.exit("no rows")
    # find a retention column matching the requested timestamp (or nearest)
    cols = rows[0].keys()
    ret_cols = [c for c in cols if "retention" in c.lower() or "watched" in c.lower()]
    if not ret_cols:
        # simple form
        scores = [(r.get("variant", "?"), float(r.get("retention_30s", 0))) for r in rows]
    else:
        target = f"{a.at_sec}"
        best_col = min(ret_cols, key=lambda c: abs(
            (int("".join(ch for ch in c if ch.isdigit()) or 0)) - a.at_sec))
        scores = [(r.get("variant") or r.get("Video title", "?"),
                   float(r[best_col].rstrip("%") or 0)) for r in rows]
    scores.sort(key=lambda x: -x[1])
    print("═" * 50)
    print(f"  HOOK ANALYTICS — retention @ {a.at_sec}s")
    print("═" * 50)
    for i, (name, r) in enumerate(scores, 1):
        medal = "🥇" if i == 1 else f"{i}."
        print(f"  {medal} {name:<40} {r:6.2f}%")
    print("─" * 50)
    winner = scores[0][0].lower()
    print(f"  WINNER: {scores[0][0]}")
    print(f"  → set defaultProps in Root.tsx: {{ hookVariant: '{winner}' }}")
    print("═" * 50)

if __name__ == "__main__":
    main()
