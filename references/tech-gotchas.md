# Tech Gotchas — 11 landmines, all field-detonated

1. **homebrew ffmpeg (8.x) has NO `subtitles`/`drawtext` filters.** Burned-in caption plans die here. Fix: render caption cards as transparent PNGs (PIL) + timed `overlay=enable='between(t,s,e)'`, or do captions in Remotion (`<CaptionOverlay/>`) — preferred.

2. **ffmpeg `xfade` chaining truncates** beyond 2 inputs (offsets compound; 5-scene graph yields 17.6s). Fix: Remotion `TransitionSeries`, or concat demuxer + per-scene edge fades as fallback.

3. **Remotion's bundled ffprobe segfaults on older macOS** — `dyld: Symbol not found: _AVCaptureDeviceTypeContinuityCamera` in `compositor-darwin-arm64/libavdevice.dylib`. Fix:
   ```bash
   cd node_modules/@remotion/compositor-darwin-arm64
   mv ffprobe ffprobe.orig && ln -s $(which ffprobe) ffprobe
   ```

4. **Remotion's final encode requests `libfdk_aac`** (nonfree; homebrew ffmpeg lacks it → exit 8). Fix: wrapper named `ffmpeg` in the same dir that rewrites `libfdk_aac`→`aac` and execs system ffmpeg (see templates/remotion-video/README.md).

5. **Remotion ignores TS type errors at bundle time** — `npx tsc --noEmit` failing on vendored code doesn't block renders. Don't chase pre-existing type noise; render to find real errors.

6. **Manim 0.21 traps:** `Text(style="italic")` → TypeError (kwarg invalid); `MathTex` requires a LaTeX install (absent → use `Text` with unicode); Arrow tip params can explode; `setup()` overrides Scene's own `setup()`. If you must Manim: simplest-possible primitives only.

7. **edge-tts over kokoro-onnx:** kokoro pip resolution fails on system Pythons; `pip3 install edge-tts` always works. `--rate=-4%` tames code-heavy copy. Always re-transcribe YOUR audio — segment times differ from any estimate.

8. **faster-whisper settings that work:** `"small"`, `compute_type="int8"`, `vad_filter=True`, `vad_parameters=dict(min_silence_duration_ms=400)`, `word_timestamps=True`. Feeding an `initial_prompt` with domain terms fixes entity mangles (OpenAI, RouterArena, JevRouter).

9. **Pillow + matplotlib frames must be normalized** to exact 1920×1080 — `bbox_inches='tight'` returns varying sizes that break concat. Post-process through PIL resize.

10. **Social cuts:** blur-pad beats center-crop (nothing clipped): `scale=1080:1920:force_original_aspect_ratio=increase,crop=…,gblur=sigma=26,eq=brightness=-0.08[bg]` + fg `scale=1080:-2` centered. See `scripts/social_cuts.sh`.

11. **Single source of truth for duration:** theme `TOTAL` (frames) is the number; Root composition `durationInFrames={TOTAL}`; scene durations sum − (n−1)×15 must equal it. Write an assert; we shipped a stale cut when they diverged.
