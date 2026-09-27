# Duno

> You built it. Now **duno** — brag about it properly.
> A hardened fork of [latent-spaces/brag](https://github.com/latent-spaces/brag), rebuilt after **11 iterations** of shipping a real product-launch video (A3M Router).

[![fork parent](https://img.shields.io/badge/fork%20of-latent--spaces%2Fbrag-blue)](https://github.com/latent-spaces/brag) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## What Duno fixes

Upstream `/brag` turns your project into a launch video with Hyperframes. Shipping a real one end-to-end surfaced every failure mode that only appears past the demo stage. Duno bakes those lessons in:

| # | Failure we hit | Duno's answer |
|---|---|---|
| 1 | Narration that reads the screen (double delivery) | **VO-first pipeline**: script the voiceover as *story*, screen shows *proof* — never the same words (`references/pipeline.md` §3) |
| 2 | Static frames with text on black scored 3.2/10 | **Remotion-first motion**: `spring()` physics, typewriters, count-ups, true `TransitionSeries` crossfades (`templates/remotion-video/`) |
| 3 | VO trimmed mid-sentence to fit video | **Video fits the VO**: whisper-transcribe the VO, place scene boundaries in speech gaps (`scripts/vo.sh`) |
| 4 | An AI-written claim off by **77×** ("a tenth of a cent" vs actual 7.68¢) | **4-lens agent council** before shipping: narrative, accuracy, visual QA, launch strategy (`council/prompts.md`) |
| 5 | Citing a benchmark whose PR was contested | **Fact-sheet gate**: every number traced to source; contested claims softened, disclaimers on illustrative figures |
| 6 | ffmpeg lacks `subtitles` filter / xfade chains break / Remotion's bundled ffprobe segfaults | **Field-tested gotchas**: 11 documented environment fixes (`references/tech-gotchas.md`) |
| 7 | "It's done" ≠ shippable | **Platform bundle**: 16:9 master + 9:16 + 1:1 blur-pad cuts, thumbnail, YouTube/HN/X/LinkedIn copy pack with attribution (`scripts/social_cuts.sh`) |
| 8 | "Looks good" is not a quality bar | **13-dimension weighted rubric** with a ≥8.0 ship gate (`references/rubric.md`, `scripts/score.py`) |

## Quickstart

```bash
# 1. Say to your agent:
/duno

# 2. Or run the pipeline manually (see SKILL.md for the full walkthrough):
cp -r templates/remotion-video my-video && cd my-video && npm install
bash ../scripts/vo.sh script.txt en-US-GuyNeural   # → voiceover.mp3 + timing map
npx remotion render src/index.tsx Video out/master.mp4 --codec h264 --crf 18
bash ../scripts/social_cuts.sh out/master.mp4 out/
python3 ../scripts/score.py   # ship gate: weighted ≥ 8.0
```

## The pipeline in one line

**facts → VO script → whisper timing → Remotion scenes on beat gaps → render → frame-verify → 4-lens council → fixes → cuts + thumbnail + copy pack → rubric ≥ 8.0 → ship.**

## Docs

- [`references/pipeline.md`](references/pipeline.md) — the full strategy: v1→v11 journey, what worked, what died
- [`references/rubric.md`](references/rubric.md) — scoring dimensions, weights, ship gate
- [`references/lessons.md`](references/lessons.md) — do's and don'ts (each one cost us a render)
- [`references/tech-gotchas.md`](references/tech-gotchas.md) — environment landmines and fixes
- [`SCORECARD.md`](SCORECARD.md) — the video that taught us all this, scored
- [`council/prompts.md`](council/prompts.md) — copy-paste council prompts
- [`ROADMAP.md`](ROADMAP.md) — the 10× plan mined from 17.8K bookmarks (LTX-2, Seedance, Marlin QA, voice-clone dubs, avatar lanes, hook-optimization loop)
- [`references/vault-research.md`](references/vault-research.md) — the deep study behind it

## Relationship to upstream

This is a fork: upstream's Hyperframes skill is preserved untouched under `skills/brag/` (and `brag-slim/`). Duno adds a parallel, motion-first pipeline and the quality system around it. Upstream's LICENSE (MIT) and examples remain intact.

## Credits

- [latent-spaces/brag](https://github.com/latent-spaces/brag) — the original skill and idea
- [Remotion](https://remotion.dev) — the composition engine Duno standardizes on
- Kevin MacLeod (incompetech.com) — default music suggestions, CC-BY
