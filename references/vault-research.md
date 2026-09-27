# Vault Deep Study — 20+ finds that 10× Duno

Source: personal bookmark vault (17,874 items), mined across 6 capability axes.
Each find: what it is → the Duno capability it unlocks. Prioritized execution in [`ROADMAP.md`](../ROADMAP.md).

## Axis 1 — Cinematic b-roll & video generation
*Current gap: Duno videos are motion-graphics only — no filmed/generated footage.*

| Find | Evidence | → Duno capability |
|---|---|---|
| **LTX-2** — first truly open-source joint audio+video foundation model; A-tier quality on your own hardware; **native lip-synced dialogue + audio** | x.com/yoavhacohen/status/2008426958267314197; x.com/ltx_model/status/2011101440706806051 | `--broll local` lane: generate hook ambiance & section transitions locally at $0; talking beats with synced audio without any API |
| **Seedance 2.0** — reads an entire shot list → generates a full story with **consistent characters, props, set design from one image** | x.com/EHuanglu/status/2054932133349883962 | Shot-list mode: VO script exports a shot list; Seedance renders a consistent cinematic thread through the video (founder "avatar" walks through all 6 beats) |
| Open-source Runway/Higgsfield alternative (free image/video gen, no subscription) | x.com/exploraX_/status/2054562825792627149 | Zero-cost fallback lane when stock footage doesn't fit the brand |
| **Remotion + Manim combo** (official Claude Code tip); NousResearch ships a Manim agent skill | x.com/claude_code/status/1947866828904272059; x.com/NousResearch/status/2040931043658567916 | Optional `--math` lane: Manim sub-renders for algorithm/architecture beats, composited as Remotion `<OffthreadVideo>` — 3B1B credibility on demand |

## Axis 2 — Voice: clone, dub, own it
*Current gap: single stock TTS voice; English only.*

| Find | Evidence | → Duno capability |
|---|---|---|
| **OmniVoice Studio** — open-source, fully offline: **3-second sample → voice clone**, video dubbing, **646 languages**, no API | x.com/NFTCPS/status/2054748417084342338 | `--voice you`: clone the founder once; every future video ships in their voice. Same master → 5-language dubs ( Localization lane) |
| **Audiblez** — open-source EPUB→audiobook entirely on a laptop | x.com/hasantoxr/status/2056245925434253450 | Reference architecture for a fully-local TTS stage (no cloud dependency, offline renders) |

## Axis 3 — Avatars & talking heads
*Current gap: no human presence — the #1 retention lever we never pulled.*

| Find | Evidence | → Duno capability |
|---|---|---|
| **HeyGen CLI** — "your AI agent can now generate and ship videos": script → avatar → video → delivery, one command | x.com/HeyGen/status/2043725015506706900 | `--avatar heygen` lane wired as a single CLI step in the pipeline — agent-native by design |
| **LongCat talking-avatar** — open-source, MIT, "probably SOTA" | x.com/victormustar/status/2058492201261244458 | Free avatar lane: founder-lookalike delivers the thesis beat; $0 path for open-source users |
| **Loopy** — audio-to-video lipsync with lifelike expressions (sighs, emotion) | x.com/EHuanglu/status/1831686214333952026 | Emotion pass on talking beats — lipsync that carries feeling, not just mouth movement |
| **InfiniteTalk** lipsync pipeline (nano-banana-pro → InfiniteTalk flow) | x.com/maxxmalist/status/2010366459743031542 | Still-image → talking beat: turn the repo's README hero image into a presenter |
| Real-time interactive avatars @180ms latency | x.com/HelloVyom/status/2058522652764230135 | Future: live "ask the repo" avatar mode at launch day |

## Axis 4 — QA: make the computer watch the render
*Current gap: manual frame sampling — we check 5 frames of 2,000.*

| Find | Evidence | → Duno capability |
|---|---|---|
| **Marlin-2B** — tiny VLM finetuned exactly for "what is happening / what is being said" in videos | x.com/HappyyPablo/status/2056839665551024474 | **Auto-QA stage**: feed `master.mp4` → structured scene log → diff against the beat map (scene order, on-screen text present, caption sync, duration drift). The council's visual lens gets a machine first pass; humans audit exceptions only |

## Axis 5 — Sound & retention craft
*Current gap: flat music bed, zero sound design, no retention engineering.*

| Find | Evidence | → Duno capability |
|---|---|---|
| **Retention editing as a discipline**: 1. story with a *why* 2. pace to the audience 3. **sound design that plays on emotions** | x.com/tropicsocial/status/1811174562144395459 | SFX layer: impact hit on the number-slam, whoosh on transitions, tick on typewriter — mapped from the same beat map that drives scenes |
| Title+thumbnail aren't the two biggest levers (packaging vs first-30s) | x.com/MarioJoos/status/1812792092910850074 | First-frame optimization: render 3 thumbnail candidates + validate the first 30s cut separately (hook A/B) |
| **Closed-loop hooks agent**: generate videos → upload every 4h → **analyze best hooks → repeat** | x.com/mamagnus00/status/2045575219042271570 | `duno loop`: 3 hook variants per video → scheduled posts → retention analytics → winning hook becomes the template default. The pipeline improves itself |
| AI music workflows (Suno/Flow/ElevenLabs full-shorts stacks) | x.com/orlandopedro/status/1949765805920403501; x.com/faiz__Ehsan/status/1984512336674029764 | Bespoke score: generate music at exact BPM/mood per video (check plan's commercial-license terms) vs stock bed |

## Axis 6 — Distribution of Duno itself
| Find | Evidence | → Duno capability |
|---|---|---|
| MCP as the universal skill socket (mobbin-MCP pulls designs into any agent) | x.com/0xSero/status/2056253989721952336 | Ship `duno-mcp`: expose `gen_vo`, `beat_map`, `render`, `score`, `council` as MCP tools — every MCP client (Claude, Cursor, Codex…) can make videos |
| Multi-client skill packaging (NousResearch Manim skill pattern) | x.com/NousResearch/status/2040931043658567916 | Complete the mirror set: `.opencode` + npm `npx skills add das-rebel/duno` |

## The compounding thesis

Individually each is a feature. Together they close a loop no competitor has:

**clone the founder's voice (OmniVoice) → script shots (VO-first) → generate cinematic b-roll locally (LTX-2/Seedance) → avatar delivers the thesis (LongCat/HeyGen) → machine-watch the render (Marlin) → council gates it → ship 3 hook variants → analytics pick the winner (loop) → dub it into 646 languages.**

That's not "a video generator." That's an autonomous launch studio.
