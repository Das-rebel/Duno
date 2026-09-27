#!/usr/bin/env bash
# Duno — sound-design pass over a rendered master: procedural SFX + ducked music.
# usage: mix_master.sh master.mp4 beats.json music.mp3 [out]
set -euo pipefail
MASTER="${1:?usage: mix_master.sh master.mp4 beats.json music.mp3 [out]}"
BEATS="${2:?beats.json required}"
MUSIC="${3:?music file required}"
OUT="${4:-${MASTER%.mp4}-sfx.mp4}"
LEN=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MASTER")
TMP=$(mktemp -d)
ffmpeg -y -i "$MASTER" -vn -c:a pcm_s16le "$TMP/vid.wav" 2>/dev/null
python3 "$(dirname "$0")/sound_design.py" --vo "$TMP/vid.wav" --music "$MUSIC" \
  --beats "$BEATS" --video-len "$LEN" --out "$TMP/mix.m4a"
ffmpeg -y -i "$MASTER" -i "$TMP/mix.m4a" -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
echo "✓ $OUT"
