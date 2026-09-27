# The Duno Pipeline — earned over 11 versions

This is the complete strategy history of one real launch video (A3M Router), v1→v11 — what each version tried, what it scored, and the strategy that survived.

## The journey

| Ver | Engine | What was added | Score | Why it failed / what stuck |
|---|---|---|---|---|
| v1 | Pillow frames | Text on black, 45s | **3.2** | "Static text, not relevant for ML devs." Stuck: real numbers only. |
| v2 | Pillow | ASCII banner, gradients, transitions | **3.2** | Cosmetic changes don't fix a static core. |
| v3 | Pillow | Real repo numbers (benchmarks, latency) | — | Content quality ≠ motion quality. Both required. |
| v4 | Pillow | Architecture diagrams (hand-drawn PIL) | — | Diagrams helped; hand-drawn charts looked amateur. |
| v5 | Pillow | Vonnegut "Man in a Hole" arc, vault-minited hooks | — | Narrative upgraded, but layout bugs (grid overflow 2120>1920px, crisscross arrows) — **measure every element against canvas bounds**. |
| v6 | matplotlib/seaborn | Publication-quality charts, exact 1920×1080 normalize | — | Chart quality solved. Still zero motion. |
| v7 | **Manim** | First real motion: typewriters, GrowFromCenter, staggered reveals | — | Motion solved for math-y scenes; Manim friction high (Arrow API, MathTex→LaTeX missing), no VO, hard cuts. |
| v8 | Manim + edge-tts | Voiceover, 5 tighter scenes | — | Three self-inflicted wounds: VO **mirrored** screen text; cheesy stock music; **time-stretched scenes 1.7× and trimmed VO mid-sentence** to force 50s. |
| v9 | ffmpeg assembly | Vault research → OpenMontage stack found; 1080p; burned captions (PIL PNGs + overlay, since ffmpeg lacked `subtitles` filter); VO un-trimmed | — | Learned: video fits the VO, not vice versa. Captions = biggest shareability unlock. |
| v10 | **Remotion** (OpenMontage's engine) | Full rebuild: spring physics, word-highlight captions, true crossfades, rewritten complementary VO, proper music | ~8.0 | The stack adoption: steal the *engine* + *patterns* (stat cards, terminal typing, captions), keep your content. |
| v11 | Remotion + **agent council** | 4-lens review caught a **77× pricing error**, contested-benchmark citation, layout bugs → all fixed; + social cuts, thumbnail, launch pack | **8.4** | Council gate is the difference between "done" and "shippable". |

## The 10 strategies that survived

1. **VO-first.** Script narration → TTS → whisper-transcribe → beat map → scene boundaries land in speech gaps. Video length = VO length + tail; never trim audio.
2. **Complement, don't mirror.** VO = story & why. Screen = proof & what. If the caption band already shows the words being said, the scene text must say something else.
3. **One engine for motion + transitions.** Remotion: `spring()`, `interpolate()`, `TransitionSeries` crossfades. ffmpeg `xfade` chains break past 2 inputs; Manim fights you on arrows/LaTeX; static frames score 3/10.
4. **The 6-beat arc.** Hook (concrete pain number) → Thesis (one line, huge) → Mechanism (the insight, animated) → Architecture (staggered detail) → Proof (2-3 count-up stats) → CTA (callback + command + URL dwell + end fade).
5. **Word-highlight captions.** Most viewers are muted. TikTok-style highlight synced to word timestamps is the single biggest shareability unlock.
6. **Fact sheet before pixels.** Every on-screen number gets a source. Mark claims verified/illustrative/contested. Disclaimers on illustrative figures, with the assumption stated.
7. **Council gate.** Four parallel lenses (narrative, accuracy, visual QA, launch). It caught a 77× error, a contested citation, and three layout bugs that "looked fine".
8. **Frame-verify like a skeptic.** Extract midpoint frames of every scene and *look* — mid-animation states hide text collisions that the source never shows.
9. **Ship the bundle, not a file.** 16:9 + 9:16 + 1:1 blur-pad cuts, thumbnail from the hook beat, copy pack with attribution and disclaimers.
10. **Steal engines, keep content.** Vault/scrub for prior art (OpenMontage, Remotion, brag); adopt the proven engine and patterns; your repo's facts are the content.

## Timing math (memorize)

- ~2 words/sec for TTS at rate −4%. 60-70s video ≈ 110-130 words.
- Crossfades 0.5s (15 frames). Scene windows sit in VO gaps.
- Scene duration: `dur_k = (start_{k+1} − start_k) + 0.5s` (last scene: VO tail + URL dwell ≥ 4s + end fade 1s).
- Caption pages ≤ 5-6 words; highlight = current word.
