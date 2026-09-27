# SCORECARD — brag-v11.mp4 (the video that produced this fork)

```
══════════════════════════════════════════════════════════════════
  DUNO SCORECARD  ·  brag-v11.mp4  ·  67.9s · 1080p30 · Remotion
══════════════════════════════════════════════════════════════════
  1  Hook                      9.0  ×1.3  ██████████████████▏░  11.70
  2  Narrative arc             9.0  ×1.0  ██████████████████░░   9.00
  3  VO↔screen complement      9.0  ×1.3  ██████████████████▏░  11.70
  4  Motion quality            8.5  ×1.2  █████████████████░░░  10.20
  5  Transitions               9.0  ×0.8  ██████████████████░░   7.20
  6  Typography & hierarchy    8.5  ×1.0  █████████████████░░░   8.50
  7  Color & contrast          9.0  ×0.8  ██████████████████░░   7.20
  8  Captions & accessibility  9.0  ×1.0  ██████████████████░░   9.00
  9  Audio                     8.0  ×1.2  ████████████████░░░░   9.60
 10  Factual integrity         9.5  ×1.3  ███████████████████░  12.35
 11  Pacing & sync             8.5  ×1.0  █████████████████░░░   8.50
 12  Platform readiness       10.0  ×0.8  ████████████████████░  8.00
 13  Reproducibility           8.0  ×0.5  ████████████████░░░░   4.00
──────────────────────────────────────────────────────────────────
  WEIGHTED TOTAL (normalized /13.2)         8.86 / 10    GRADE: B (top of band, 0.14 to A)
  SHIP GATE (≥8.0, no dim <6)                    ✅ PASS
══════════════════════════════════════════════════════════════════
```

Deductions, honestly:
- **Motion 8.5** — particles are static-position pulses; no camera moves (Ken Burns / push-ins) yet.
- **Audio 8.0** — single TTS voice, zero ducking automation under VO peaks; music bed is stock CC-BY.
- **Repro 8.0** — rebuild is documented but multi-command; needs a one-shot `make`.
- **Pacing 8.5** — CTA beat carries 5 on-screen events; one more second of dwell would loosen it.

Path to A (≥9.0): camera motion layer, audio ducking sidechain, `make video` one-shot, B-roll inserts on hook/CTA.
