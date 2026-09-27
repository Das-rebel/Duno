#!/usr/bin/env python3
"""Duno rubric scorer. Usage: score.py [s1 s2 ... s13]  (defaults: v11 reference scores)"""
import sys

DIMS = [
    ("Hook",                     1.3), ("Narrative arc",            1.0),
    ("VO-screen complement",     1.3), ("Motion quality",           1.2),
    ("Transitions",              0.8), ("Typography & hierarchy",   1.0),
    ("Color & contrast",         0.8), ("Captions & accessibility", 1.0),
    ("Audio",                    1.2), ("Factual integrity",        1.3),
    ("Pacing & sync",            1.0), ("Platform readiness",       0.8),
    ("Reproducibility",          0.5), ("Frame visibility",        1.0),
]
V11 = [9, 9, 9, 8.5, 9, 8.5, 9, 9, 8, 9.5, 8.5, 10, 8, 9]

def bar(score):
    filled = round(score / 10 * 20)
    return "█" * filled + "░" * (20 - filled)

def main():
    scores = [float(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else V11
    if len(scores) != len(DIMS):
        sys.exit(f"need 13 scores, got {len(scores)}")
    for s in scores:
        if not 0 <= s <= 10:
            sys.exit("scores must be 0-10")
    max_total = sum(w for _, w in DIMS)
    total = sum(s * w for s, (_, w) in zip(scores, DIMS)) / max_total
    grade = "A" if total >= 9 else "B" if total >= 8 else "C" if total >= 6.5 else "D"
    gate = total >= 8.0 and min(scores) >= 6
    print("═" * 66)
    print("  DUNO SCORECARD")
    print("═" * 66)
    for s, (name, w) in zip(scores, DIMS):
        print(f"  {name:26s} {s:4.1f}  ×{w:<4.1f} {bar(s)} {s*w:6.2f}")
    print("─" * 66)
    print(f"  WEIGHTED TOTAL  {total:5.2f} / 10    GRADE: {grade}")
    print(f"  SHIP GATE (≥8.0, no dim <6):   {'✅ PASS' if gate else '❌ FAIL'}")
    print("═" * 66)
    low = [(n, s) for s, (n, _) in zip(scores, DIMS) if s < 6]
    if low:
        print("  BLOCKING (dim <6):", ", ".join(f"{n}={s}" for n, s in low))
    sys.exit(0 if gate else 1)

if __name__ == "__main__":
    main()
