# duno-video template

Drop-in Remotion scaffold with the Duno pipeline prewired: word-highlight
captions, TransitionSeries crossfades, EndFade, audio slots, a hardened
postinstall that fixes ffmpeg/libavdevice dyld crashes on macOS.

```bash
npm install              # postinstall auto-patches ffmpeg/ffprobe symlinks
npm run render           # out/master.mp4 (Remotion render)
npm run thumb            # out/thumb-raw.png (hook beat still)
```

Set your beat map in `src/theme.ts` (DUR frames @30fps; TOTAL = Σ − (n−1)×15).
Caption segments go in `src/captions.tsx` — paste your whisper timing.json segments.

## Quickest path to ship

```bash
bash ../../scripts/vo.sh script.txt en-US-GuyNeural   # VO + whisper timing
bash ../../scripts/mix_master.sh out/master.mp4 beats.json music.mp3  # SFX + duck
python3 ../../scripts/qa_video.py --video out/master.mp4 --beats qa.json  # PASS/DRIFT
python3 ../../scripts/audit_render.py out/master.mp4 --out frames/  # ← THE STEP THAT MATTERS
python3 ../../scripts/score.py                                            # rubric ship gate
```

## Before publishing — AUDIT YOUR FRAMES (the step I always want to skip)

The biggest category of bug in this pipeline is **visual elements rendered off-screen** — a `top: 540` inside a `paddingTop: 48` parent pushed the child to y=886, **off the 1080p canvas**. Source code review can't catch these. Animated `spring()` delays can fire 3 seconds too late, after the VO has moved on.

The fix: extract 15-20 frames at evenly-spaced timestamps across the composition, view each one, and check the checklist printed by `audit_render.py`. Five minutes of looking saves a re-render cycle after a community member spots the bug.

```bash
python3 ../../scripts/audit_render.py out/master.mp4 --out frames/
open frames/t_*.jpg
```

Per frame, ask: "Is the visual the VO is describing actually ON SCREEN right now?" If the answer is no, that's a broken beat — fix the spring delay or the parent padding.

## The non-negotiable rules (learned the hard way)

1. **Use `flex` centering, not `paddingTop` + `position: absolute`.** Flex layout makes off-canvas content structurally impossible. See `src/scenes/ExampleScene.tsx` for the pattern.
2. **Anchor animation springs to global VO timestamps**, not scene-local frames. Convert whisper `start` times to scene-local by subtracting the scene's visual start. Every visual must land within ±0.5s of the VO beat it illustrates.
3. **The closing slam must fully replace, not overlay.** Give the closing scene its own `position: absolute, inset: 0, zIndex: 10` and higher-z elements that occlude the previous scene.
4. **Run `npx tsc --noEmit` before every render.** Remotion ignores type errors at bundle time, so a typo'd variable crashes the render mid-output with `ReferenceError`. TSC catches it instantly.
5. **Real B-roll fixes the whole scene.** A 10-second real clip of a comedian performing, with the model's laugh predictions layered over it, lands the moment in a way no animated silhouette can. Use licensed or self-recorded footage.

## First-render fixes (macOS)

If ffprobe crashes (dyld/AVFoundation):
```bash
cd node_modules/@remotion/compositor-darwin-arm64
[ -e ffprobe.orig ] || mv ffprobe ffprobe.orig
ln -s "$(which ffprobe)" ffprobe
# ffmpeg wrapper is auto-installed by postinstall with absolute path baked in
```

If the final encode fails on `libfdk_aac` (exit 8): the wrapper at `compositor-darwin-arm64/ffmpeg` rewrites `libfdk_aac` → `aac` and forwards to system ffmpeg. Verify it's present and executable.

## Layout rules of thumb

- `display: flex` + `alignItems: center` + `justifyContent: center` for ALL scenes — content fills the full 1920×1080 frame
- For positioned children inside a flex parent: use `position: absolute` with `top:`/`left:` values relative to the page (not relative to a parent with padding)
- For animation timing: `spring({ frame: frame - <delay>, ... })` where `<delay>` is the scene-local frame where the visual should start to appear (computed from whisper timestamps)
