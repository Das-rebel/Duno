# Duno Rubric — 13 dimensions, weighted, ship gate 8.0

Score each 0-10. Weighted total = Σ(score × weight). **Ship only if total ≥ 8.0 AND no dimension < 6.**
Run: `python3 scripts/score.py 9 9 9 8.5 9 8.5 9 9 8 9.5 8.5 10 8`

| # | Dimension | Wt | 0-4 (fail) | 5-7 (meh) | 8-10 (ship) |
|---|---|---|---|---|---|
| 1 | **Hook** | ×1.3 | Static title card | Number appears, no impact | Concrete pain number slams in <5s; earns the next 60 |
| 2 | **Narrative arc** | ×1.0 | Feature list | Arc but no closure | Beat arc with opening→CTA callback ("$4,217 → $27") |
| 3 | **VO ↔ screen complement** | ×1.3 | VO reads the screen | Partial duplication | VO = story/why; screen = proof/what; zero mirrored sentences |
| 4 | **Motion quality** | ×1.2 | Static frames | Some tweens, linear easing | Every element animates; spring/stagger; no hold >2s |
| 5 | **Transitions** | ×0.8 | Hard cuts | Fade to black dips | True crossfades, timed to VO gaps |
| 6 | **Typography & hierarchy** | ×1.0 | Default fonts, flat sizes | Readable but flat | Mono for code/numbers, 3+ size hierarchy, dominant focal per beat |
| 7 | **Color & contrast** | ×0.8 | Unchecked | Pretty but low-contrast | One accent system; dim text ≥7:1 (WCAG AA); red=pain, green=win |
| 8 | **Captions & accessibility** | ×1.0 | None | Block captions | Word-highlight, ≤6 words/page, synced to whisper timestamps |
| 9 | **Audio** | ×1.2 | No VO / clipped VO | VO ok, music random | TTS VO clean; bed music 10-15% w/ fade-in; genre fits devs; no mid-sentence cuts |
| 10 | **Factual integrity** | ×1.3 | Any unsourced number | Sourced but overclaimed | Fact sheet traced; illustrative figures disclaimed with assumptions; contested claims softened |
| 11 | **Pacing & sync** | ×1.0 | Scenes fight the VO | Rough sync | Boundaries in speech gaps; URL dwell ≥4s; no rushed stretches |
| 12 | **Platform readiness** | ×0.8 | One file | Master + 1 cut | 16:9 + 9:16 + 1:1 + thumbnail + copy pack w/ attribution & disclaimers |
| 13 | **Reproducibility** | ×0.5 | Unreproducible | Rebuild by archaeology | One-command rebuild; durations single-sourced; honest limitations in copy |

## Grades

| Weighted | Grade | Meaning |
|---|---|---|
| ≥ 9.0 | A | Veritasium-adjacent. Ship everywhere. |
| 8.0–8.9 | B | Polished launch. Ship. |
| 6.5–7.9 | C | Internal/demo only. |
| < 6.5 | D | It's a slideshow. Rebuild. |
