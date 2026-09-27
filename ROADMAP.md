# DUNO 10× ROADMAP — from vault deep study ([references/vault-research.md](references/vault-research.md))

Scoring: impact = capability multiplier; effort = focused days. P0 first.

## P0 — Close the loop (≈ 1 week, biggest 10×)

### R1 · Machine-watched QA — **Marlin-2B / VLM pass** ⭐ new stage
The pipeline's weakest step is "extract 5 frames and eyeball." Replace with: render → VLM watches the full video → structured scene log → diff against beat map (order, text presence, caption sync, duration drift) → council only audits exceptions.
- Impact: QA coverage 0.25% → 100% of frames; catches mid-animation collisions we shipped twice.
- Effort: 2-3d (Marlin local, or any VLM API with video input as fallback).
- Accept: `duno qa master.mp4` prints per-beat PASS/DRIFT table in <3 min.

### R2 · Sound-design layer — SFX + ducking ⭐ new track
Retention-editing craft: impact on the $-slam, whoosh on crossfades, typewriter ticks; sidechain-duck music under VO.
- Impact: perceived production value +~1 rubric grade; fixes Audio 8.0 deduction.
- Effort: 2d (freesound.org CC0 pack + ffmpeg `sidechaincompress`; beat map already has timestamps).
- Accept: rubric Audio ≥ 9; SFX fire within 1 frame of beat-map events.

### R3 · Hook variant engine + analytics loop
3 hook cuts per video (different first-5s), YouTube API scheduled posts, retention analytics → winning hook becomes the template default (mamagnus00 closed-loop pattern).
- Impact: turns one-off videos into a self-improving distribution system.
- Effort: 3d (variants = trivial re-renders of beat 1; upload via YouTube Data API; analytics cron).
- Accept: `duno loop` ships 3 variants and reports 48h retention per hook.

### R4 · One-shot rebuild — `make video`
Fixes Reproducibility 8.0: single entry point runs vo.sh → render → qa → cuts → score.
- Effort: 0.5d. Accept: clean clone → `make video URL=…` → bundle, zero docs read.

## P1 — New lanes (≈ 2 weeks)

### R5 · Voice lane — OmniVoice clone + dubs
Founder 3s sample → cloned voice default; master video → 646-language dubs. Fully offline.
- Impact: personal brand + 10× audience reach. Effort: 3-4d. Accept: same video in 3 languages from one command.

### R6 · B-roll lane — LTX-2 local generation
`--broll local`: hook ambiance + transition plates generated on own hardware; CLIP-searchable stock corpus (archive.org/Pexels) as fallback (OpenMontage pattern).
- Impact: fills the "no footage" gap at $0. Effort: 4-5d (GPU-gated; document min spec). Accept: hook beat uses generated plate; cost $0.

### R7 · Avatar lane — LongCat (MIT) default, HeyGen CLI premium
Talking-head thesis beat; still-image → presenter via InfiniteTalk/Loopy lipsync.
- Impact: the human-presence retention lever. Effort: 4d. Accept: `--avatar` renders a talking beat with lipsync; off by default.

### R8 · `duno-mcp` — ship the pipeline as MCP tools
`gen_vo`, `beat_map`, `render`, `qa`, `score`, `council` as MCP tools (mobbin-MCP pattern) + complete client mirrors (.opencode, `npx skills add das-rebel/duno`).
- Impact: every MCP client becomes a video studio — distribution 10× of Duno itself. Effort: 3d. Accept: Claude Desktop makes a full video via tools only.

## P2 — Cinematic tier (later)

### R9 · Shot-list cinematic mode — Seedance 2.0
VO script exports a shot list; consistent characters/props across all beats from one reference image. Effort: 5-6d, API cost per render.

### R10 · Math lane — Manim sub-renders (official Claude-Code combo)
`--math`: Manim renders algorithm/architecture beats → `<OffthreadVideo>` composite. Effort: 3d.

### R11 · Bespoke score — Suno/udio per-video music
Exact BPM/mood generation (verify commercial license tier). Effort: 1-2d.

### R12 · Live mode — 180ms real-time avatar
Launch-day "ask the repo" live avatar. Effort: research spike.

## Dependency graph

```
R4 ─┐
R1 ─┼→ R3 (loop) → R5 (dubs ride the loop)
R2 ─┘
R6 ──→ R9      R7 ──→ R12      R8 (independent, do anytime after R4)
```

## 10× math

| Axis | Today | Post-P0+P1 |
|---|---|---|
| QA coverage | 0.25% frames, manual | 100%, automated (R1) |
| Voices | 1 stock | founder clone × 646 languages (R5) |
| Footage | 0 | local gen + stock corpus (R6) |
| Human presence | none | avatar lane (R7) |
| Distribution | 1 manual upload | 3-variant self-optimizing loop (R3) |
| Reach of Duno | 1 skill dir | every MCP client (R8) |
