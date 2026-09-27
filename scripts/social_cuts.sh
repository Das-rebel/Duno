#!/usr/bin/env bash
# Duno social cuts: 16:9 master → 9:16 + 1:1 (blur-pad, nothing clipped)
# usage: social_cuts.sh master.mp4 out_dir
set -euo pipefail
MASTER="${1:?usage: social_cuts.sh master.mp4 out_dir}"
OUT="${2:-.}"
mkdir -p "$OUT"
BASE="$(basename "$MASTER" .mp4)"
ffmpeg -y -i "$MASTER" -filter_complex \
  "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=26,eq=brightness=-0.08[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k \
  "$OUT/$BASE-vertical.mp4"
ffmpeg -y -i "$MASTER" -filter_complex \
  "[0:v]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,gblur=sigma=26,eq=brightness=-0.08[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 160k \
  "$OUT/$BASE-square.mp4"
echo "✓ $OUT/$BASE-vertical.mp4 (9:16)  ✓ $OUT/$BASE-square.mp4 (1:1)"
