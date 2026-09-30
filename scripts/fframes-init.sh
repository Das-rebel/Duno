#!/usr/bin/env bash
# Duno wrapper for fframes (Rust + Skia GPU-rendered video framework).
# Use when motion-graphics-heavy scenes benefit from GPU rendering or when the
# author needs to embed fframes into the Duno pipeline.
#
# Usage:
#   bash scripts/fframes-init.sh <project-name> [output-dir]
#
# Creates <project-name> using the fframes CLI, copies the Duno scene-template
# scaffold, and leaves a ready-to-render project at <output-dir>/<project-name>.
set -euo pipefail

NAME="${1:?usage: fframes-init.sh <project-name> [output-dir]}"
OUT="${2:-$(pwd)}"

if ! command -v cargo >/dev/null; then
  echo "❌ cargo not found. Install Rust via https://rustup.rs first."
  exit 1
fi

if ! command -v ffmpeg >/dev/null; then
  echo "⚠️  ffmpeg not found. fframes can install its own prebuilt libs, but system ffmpeg helps."
fi

echo "→ Installing cargo-fframes (Rust CLI scaffold)..."
cargo install --locked cargo-fframes 2>&1 | tail -3

PROJECT="$OUT/$NAME"
mkdir -p "$PROJECT"
cd "$PROJECT"

echo "→ Scaffolding fframes project: $NAME"
cargo fframes new "$NAME" \
  --template single-scene \
  --format landscape \
  --fps 30 \
  --title "$NAME"

# Drop in the Duno scene scaffold
mkdir -p "$PROJECT/src/scenes"
cat > "$PROJECT/src/scenes/duno_example.rs" << 'SCENEEOF'
// Duno scaffold scene — render a centered title card with fade-in.
use fframes::svgr;
use fframes::timeline;
use fframes::Easing;
use fframes::Transform;

pub fn duno_title_card() -> fframes::Svgr<'static> {
    svgr!(
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">
            <rect width="1920" height="1080" fill="#0A0E0A"/>
            <text x="960" y="540" font-family="JetBrains Mono" font-size="80"
                  font-weight="700" fill="#A78BFA" text-anchor="middle">
                Duno
            </text>
            <text x="960" y="640" font-family="JetBrains Mono" font-size="32"
                  fill="#8CAA96" text-anchor="middle">
                GPU-rendered title card via fframes
            </text>
        </svg>
    )
}
SCENEEOF

cat > "$PROJECT/duno.md" << 'READMEEOF'
# $NAME

Duno scaffold for an fframes video project.

## Build & render
\`\`\`bash
cargo run --release -- render
\`\`\`

## Edit scenes
- Drop scene files in \`src/scenes/\`
- Register them in \`src/main.rs\` (or \`src/lib.rs\`)
- Use the \`svgr!\` macro to write SVG with Rust expressions for animation

## Duno integration
- ffmpeg wrapper: \`scripts/fix-remotion-binaries.js\` is NOT needed (fframes links ffmpeg directly)
- transitions: use the \`timeline!\` macro instead of ffmpeg's xfade filter
- captions: render as SVG text in the scene, not via Remotion's CaptionOverlay
READMEEOF

echo "✓ fframes project scaffolded at $PROJECT"
echo "  → cd $PROJECT && cargo run --release -- preview"
echo "  → render to .mp4: cargo run --release -- render"
