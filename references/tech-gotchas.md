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

12. **`sidechaincompress` truncates the whole graph at the sidechain's RAW input length** — pre-padding the key inside the graph (`apad=whole_dur`) does NOT save you; output still ends at the unpadded EOF (63.0s ghost). Fix: pre-pad the VO to a WAV file in a separate pass, then feed that file in. Verified ffmpeg 8.1.1.

13. **Remotion ffmpeg-wrapper recursion**: if your `ffmpeg` wrapper resolves ffmpeg via `command -v ffmpeg` at runtime, Remotion puts the compositor dir FIRST on PATH → the wrapper finds ITSELF → infinite exec loop (silently burned 2:37 CPU). Fix: bake the ABSOLUTE system ffmpeg path into the wrapper at install time. `templates/remotion-video/scripts/fix-remotion-binaries.js` does both fixes automatically via npm `postinstall`.

14. **Remotion placeholder audio shorter than the composition can stall the stitcher** after "Rendered N/N" — ship placeholder audio at (or above) full composition length.

15. **Remotion render cache disk pressure:** A 1080p/30fps render produces ~5–6 GB of cached JPEG frames in `/var/folders/.../T/remotion-*`. On `/tmp` partitions ≤ 5 GB free, renders fail with `ENOSPC: no space left on device` partway through. Two mitigations: (a) free ≥ 8 GB before launching (clear `/var/folders/.../T/remotion-*` and other T-cached artifacts), or (b) render at `--scale 0.7` to fit. Scale-down renders are visibly identical to full-res for a final shipping review.

16. **TypeError mid-render silent failure:** When a Remotion scene has a typo'd identifier (e.g., `interpolate(birp, ...)` instead of `birb`), the bundle compiles fine (Remotion ignores TS errors at bundle) but the render crashes at the first frame where the missing variable is evaluated with `ReferenceError: X is not defined`. This stops rendering mid-output with a half-finished mp4. Always `npx tsc --noEmit` before rendering — TSC catches the typo instantly, the runtime doesn't until that frame.

17. **Captions drift across transition fades.** When `TransitionSeries` uses 0.5s crossfades between scenes, the caption text for the NEXT scene's first segment starts rendering DURING the previous scene's tail — so a frame at e.g. t=14s in v5 showed the S3 caption ("the transcripts. The transcript is") over the S2 visual content. Two fixes: (a) offset caption `startMs` by the fade duration so the caption waits for the scene to be fully visible, or (b) add a `delayed` segment in the captions builder that mirrors each scene's visual fade-in.

18. **Position:absolute with `top:` values relative to a parent that has `padding` or `marginTop`** is the #1 cause of "the visual is in the source but not in the render." In v5 HaHaScore S4, the waveform timeline was at `top: 540` inside a `paddingTop: 48` parent — the parent shifted the child by 48px, so the child landed at y≈588 (within frame) but the parent's `marginTop: 26` from a preceding sibling pushed it to y≈886, **off the 1080p canvas**. Always either: (a) position absolutely against `AbsoluteFill` (the page) with explicit `top: VALUE` matching where you want it on the page, or (b) use flex layout so children flow naturally within the parent's bounds.
