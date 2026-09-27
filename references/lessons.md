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
