# duno-video template

Drop-in Remotion scaffold with the Duno pipeline prewired: word-highlight captions,
TransitionSeries crossfades, end fade, audio beds, and a thumb composition.

```bash
npm install
# put voiceover.mp3 + music.mp3 in public/
npx remotion studio           # live preview
npm run render                # out/master.mp4
npm run thumb                 # out/thumb-raw.png (hook beat still)
```

Set your beat map in `src/theme.ts` (DUR frames @30fps; TOTAL = Σ − (n−1)×15).
Caption segments go in `src/captions.ts` — paste your whisper timing.json segments.

## First-render fixes (macOS)

If ffprobe crashes (dyld/AVFoundation):
```bash
cd node_modules/@remotion/compositor-darwin-arm64
[ -e ffprobe.orig ] || mv ffprobe ffprobe.orig
ln -s "$(which ffprobe)" ffprobe
```

If the final encode fails on `libfdk_aac` (exit 8), replace `ffmpeg` there with:
```bash
#!/bin/bash
args=(); for a in "$@"; do [[ "$a" == "libfdk_aac" ]] && a=aac; args+=("$a"); done
exec "$(which ffmpeg)" "${args[@]}"
```
(`chmod +x` it.)
