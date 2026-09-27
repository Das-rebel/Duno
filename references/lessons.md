# Do's and Don'ts — each one cost a render

## DON'T

1. **Don't ship static frames.** Text-on-black scored 3.2/10 twice before motion existed. If nothing moves per beat, it's a slideshow.
2. **Don't let narration read the screen.** Double delivery reads as amateur within 5 seconds. (v8 sin, fixed v10.)
3. **Don't trim the VO to fit the video.** Cutting audio mid-sentence is fatal. Extend the video; freeze the CTA frame.
4. **Don't time-stretch rendered scenes** to hit a duration (1.7× speed looked crack-fueled). Retime at the source or re-map beats.
5. **Don't chain ffmpeg `xfade`** for >2 inputs — offsets compound wrong and output truncates. Use Remotion `TransitionSeries`.
6. **Don't hand-draw charts in PIL.** matplotlib/seaborn exist. Better: make the chart a Remotion component with count-ups.
7. **Don't trust generated numbers.** "Less than a tenth of a cent" vs actual 7.68¢ — a 77× error that a fact-checking HN mob would have caught. Council the numbers.
8. **Don't cite a benchmark without checking provenance.** A closed PR ≠ a ranking.
9. **Don't use "happy corporate beats"** for a dev audience. Driving electronic, no vocals, 10-15% volume.
10. **Don't skip the frame check.** Source code never shows the frame where two springs overlap and collide.
11. **Don't hardcode durations in two places.** `durationInFrames` in Root must derive from the theme's TOTAL. We shipped a stale video because of this.
12. **Don't assume tool availability.** Probe ffmpeg filters, latex, TTS deps *before* building the pipeline around them.
13. **Don't center content horizontally and forget vertically.** Top-heavy scenes read as templates. `justifyContent: center`.
14. **Don't launch without the bundle.** Muted-viewer captions, vertical cut, thumbnail, and a disclaimer-bearing description are part of "done".


15. **Don't put visual elements at deep `top: 500+` offsets** in a parent with `paddingTop` or `marginTop`. The offset compounds with the parent's offset. Either use flex centering OR use absolute positioning relative to the page (not the parent).
16. **Don't render the closing as overlay on the previous scene.** It needs to occlude. Otherwise the previous scene's static elements compete with the closing's animated elements.
17. **Don't run a render without first running `npx tsc --noEmit`** even though Remotion ignores type errors at bundle time. Real runtime errors (e.g., a typo'd variable `birp` vs `birb` in a scene) crash the render at frame N mid-render with `ReferenceError: birp is not defined` — leaving you with a corrupted half-output and no clear pointer to the source. TSC catches it instantly.
18. **Don't ship without rendering at multiple offsets and visually auditing each one.** A render that "looks fine" at frame 0 can have catastrophic layout collapse at frame 200. The 5 minutes it takes to extract 15-20 frames at evenly-spaced timestamps is cheaper than one re-render cycle after a community member spots the bug.

## DO

1. **Write the VO first.** It's the spine; visuals hang off its beat map.
2. **Whisper your own VO** for word-level timestamps — captions and scene boundaries fall out for free.
3. **Slam one number.** A concrete pain figure ($4,217) with spring+shake beats any adjective.
4. **Callback the opener at the CTA.** Same number, transformed ($4,217 → $27). The arc is the memory.
5. **Show the install command typing itself.** Character-by-character terminal = universal dev trust signal.
6. **Count up your stats.** Spring-in stat cards with animated counters, sources cited on-screen.
7. **Freeze the URL ≥4s** with an end fade. Give the screenshot-moment time to happen.
8. **Council before shipping** — 4 parallel lenses, criticals block, fixes re-render, re-audit only what changed.
9. **Steal engines shamelessly.** OpenMontage's Remotion patterns (stat cards, terminal typing, caption overlay) are public — adopt, attribute, improve.
10. **Keep an examples/ folder** of past versions with scores — it's how you prove the pipeline works and onboard collaborators.

11. **Audit by extracting frames at every beat midpoint**, not at hand-picked moments. The v5 HaHaScore rendered with 8 scenes — I screenshotted at the S2, S3, and S7 midpoints (the ones that looked good). Auditing at 17 timestamps revealed 5 catastrophic breaks I'd missed: waveform timeline rendered off-screen, σ gate appearing 3s after the VO mentioned it, struck-through climax text missing, 355M/1M numbers missing entirely. Mid-animations and overlaps are the real killers — frame 0 and frame 50 lie.
12. **Use `flex: column/row` with `alignItems: center, justifyContent: center` for EVERY scene**, not `paddingTop` and `position: absolute` children. In v4 HaHaScore, the S4 waveform timeline was positioned `top: 540` inside a `paddingTop: 48` parent — the parent pushed the child to y≈886, off the 1080p canvas. Always visible to the source, never visible in the render. Flex centering makes it impossible to clip.
13. **Anchor animation springs to global VO timestamps, not scene-local frames.** The S3 σ gate in v5 used `spring({frame: frame - 360, fps, ...})` — that was local frame 360 of 420 = 12s into S3 = global 29.5s, but the VO said "the wager" at global 22s. Fix: compute spring delays as `(whisper_end_global - scene_visual_start) * fps`. Every visual should land within ±0.5s of the VO beat it illustrates.
14. **The closing slam must fully replace, not overlay.** In v5 S7, the "the laugh is in the room" closed over the still-visible YouTube player for ~3 seconds — they competed for the same screen space. Fix: give the closing its own scene with `position: absolute, inset: 0, zIndex: 10` and the closing slam elements at higher z, so the previous scene's content is occluded by the new scene's background.
15. **Real B-roll fixes the whole scene.** In S4 (the gold set), the on-stage footage of Mike Birbiglia performing live made the moment land. Without it, the same animation timeline read as a chart, not a comedy club. Use real-licensed or self-recorded comedian footage when the scene IS the demo of "we tested this on real standup." A silhouette of the same scene reads as placeholder; a 10s real clip reads as proof.

