#!/usr/bin/env bash
# Duno R3 — render N hook variants for A/B testing.
# usage: render_variants.sh [scale] [variants]
# Each variant re-renders the full composition with a different beat-1 hook.
# Then ship all three; scripts/analytics.py picks the winner from retention data.
set -euo pipefail
SCALE="${1:-1.0}"
VARIANTS="${2:-slam question delta}"
cd "$(dirname "$0")/../templates/remotion-video"
for V in $VARIANTS; do
  OUT="out/master-${V}.mp4"
  echo "▶ variant: $V → $OUT"
  npx remotion render src/index.tsx Video "$OUT" \
    --props="{\"hookVariant\":\"$V\"}" --codec h264 --crf 18 --scale="$SCALE" --log=error
done
echo "✓ variants: $VARIANTS"
