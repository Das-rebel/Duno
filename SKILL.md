---
name: duno
description: Turn the project you just built into a polished, fact-checked, multi-format launch video (master + social cuts + thumbnail + copy pack) using a VO-first Remotion pipeline with an agent-council quality gate. Use when someone says "/duno", "make a launch video", "brag about this", or wants to ship a video of their project. Hardened fork of /brag.
---

# /duno

You built it. Now prove it — in 60-75 seconds, with narration, motion, and receipts.

Duno is `/brag` hardened by shipping a real one. The pipeline is **VO-first**: write the narration before any visuals, transcribe it for timing, then build motion that *complements* — never repeats — the spoken words.

## Phase 0 — Environment probe (5 min, saves hours)

Check, in order, and apply `references/tech-gotchas.md` fixes preemptively:

1. `ffmpeg -filters | grep -cw subtitles` — homebrew builds lack it. Don't burn captions with ffmpeg; use the template's `<CaptionOverlay/>` (Remotion).
2. Remotion renders on macOS may crash on bundled ffprobe (dyld/AVFoundation). Fix: symlink system `ffprobe` into `node_modules/@remotion/compositor-darwin-arm64/`. If final encode fails on `libfdk_aac`, install the ffmpeg wrapper script (gotcha #4).
3. TTS: `python3 -m edge_tts` (pip install edge-tts). Voice `en-US-GuyNeural --rate=-4%` reads code-heavy copy well.
4. Timing: `faster-whisper` ("small", int8, `vad_filter=True`, `min_silence_duration_ms=400`, `word_timestamps=True`).

## Phase 1 — Facts before fiction

Read the project. Build a **fact sheet**: every number, command, and claim you might put on screen, each with its source file. Rules:

- No number goes on screen without a source in this sheet.
- Mark each claim `verified` / `illustrative` / `contested`. Contested claims get softened or dropped — check the provenance (a benchmark PR that's closed ≠ a ranking).
- Illustrative figures ($bills, $savings) always get an on-screen disclaimer with the assumption (e.g., "~350K queries/mo at benchmark rates").

## Phase 2 — Script the VO (before any visuals!)

Write ~110-130 words for a 60-70s video. The iron rule:

> **The narration tells the story. The screen shows the proof. They never say the same thing.**

- If a number matters ($4,217), the VO explains *why* it happened while the screen slams the number in.
- Sentences ≤ 20 words. Concrete metaphors, bookended (opening callback closes at the CTA).
- Name the thesis out loud, once ("It's a router.").
- No marketing adjectives a skeptic would cross out.

Generate: `bash scripts/vo.sh script.txt en-US-GuyNeural` → `voiceover.mp3` + printed segment timing map.

## Phase 3 — Beat map → scenes

Place every scene boundary **inside a speech gap** (VO beats have 0.5-1.5s gaps). Scene window formula with 0.5s crossfades: `dur_k = (start_{k+1} − start_k) + 0.5`. Convert to frames @30fps. The 6-beat arc that works:

1. **Hook** (pain, concrete number slams in) → 2. **Thesis** (one line, huge) → 3. **Mechanism** (the insight, animated diagram) → 4. **Architecture** (how it works, staggered reveals) → 5. **Proof** (2-3 count-up stats, sourced) → 6. **CTA** (callback + terminal typing + URL, freeze ≥4s, end fade).

## Phase 4 — Build with the template

```bash
cp -r templates/remotion-video my-video && cd my-video && npm install
```

- `src/theme.ts` — palette (ONE accent green, red = pain, dim text WCAG-AA ≥7:1 on the dark bg), FPS, scene durations. **`durationInFrames` in Root must equal `TOTAL` here — single source of truth.**
- `<CaptionOverlay/>` word-highlight captions: build from the whisper segments (`src/captions.ts` pattern). Muted viewers are the majority.
- Every element animates: `Write`/typewriter for code, `spring()` slams for numbers, staggered `LaggedStart` for lists, count-up for stats. No static holds longer than 2s.
- Music: driving electronic bed (Kevin MacLeod: *Voltaic*/*Cipher* class), volume **0.10-0.15**, 1.5s fade-in, never vocal.
- Render: `npx remotion render src/index.tsx Video out/master.mp4 --codec h264 --crf 18`

## Phase 5 — Verify like a skeptic

Extract frames at scene midpoints (`ffmpeg -vf select=eq(n\,N)`) and **actually look at them** (image-read). Check: text collision, overflow, top-heavy layouts (center content vertically), caption legibility over particles, mid-animation states — the frame between reveals is where bugs live.

## Phase 6 — Council gate (mandatory)

Run 4 reviewer agents **in parallel** with the prompts in `council/prompts.md`:
**Narrative** (hook, arc, VO/screen interplay) · **Accuracy** (every number vs fact sheet) · **Visual QA** (frames + source) · **Launch strategist** (titles, description, HN, thread, thumbnail).

Triage: critical (wrong numbers, provenance, broken layout) → fix + re-render. Then re-run only the auditor that flagged.

## Phase 7 — Ship bundle

```bash
bash scripts/social_cuts.sh out/master.mp4 out/     # 9:16 + 1:1 blur-pad
# Thumbnail: still of the hook beat + CTA text overlay + bottom-right caption
python3 scripts/score.py   # weighted rubric — ship gate ≥ 8.0
```

Copy pack: YouTube description (2 hook lines, timestamps, **music attribution**, **illustrative-figure disclaimer**), Show HN (facts + honest limitations + ask), 5-post X thread (post 1 standalone), LinkedIn blurb.

## Ship gate

`scripts/score.py` weighted total ≥ **8.0**, no dimension < 6, zero unresolved critical council flags. Below gate → fix, don't ship.
