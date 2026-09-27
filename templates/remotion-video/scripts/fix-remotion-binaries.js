#!/usr/bin/env node
/**
 * Duno postinstall: patches Remotion's bundled ffmpeg/ffprobe on macOS,
 * where the prebuilt ffprobe segfaults (dyld/AVFoundation) and the final
 * encode requests nonfree libfdk_aac. Idempotent; no-ops elsewhere.
 */
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "..", "node_modules", "@remotion", "compositor-darwin-arm64");
if (process.platform !== "darwin" || !fs.existsSync(dir)) {
  console.log("[duno-fix] not darwin-arm64 or no compositor dir — skipping");
  process.exit(0);
}
const sys = (b) => { try { return execSync(`which ${b}`).toString().trim(); } catch { return null; } };

const ffprobe = path.join(dir, "ffprobe");
if (fs.existsSync(ffprobe) && !fs.existsSync(ffprobe + ".orig") && fs.lstatSync(ffprobe).isFile()) {
  fs.renameSync(ffprobe, ffprobe + ".orig");
}
if (!fs.existsSync(ffprobe)) {
  const sysFfprobe = sys("ffprobe");
  if (sysFfprobe) { fs.symlinkSync(sysFfprobe, ffprobe); console.log("[duno-fix] ffprobe →", sysFfprobe); }
}

// CRITICAL: bake the ABSOLUTE system ffmpeg path. A runtime `command -v ffmpeg`
// resolves to THIS WRAPPER (Remotion puts the compositor dir first on PATH)
// and infinitely recurses (burned 2:37 CPU spinning before we caught it).
const sysFfmpeg = sys("ffmpeg");
if (!sysFfmpeg) { console.log("[duno-fix] system ffmpeg not found — skipping wrapper"); process.exit(0); }
const ffmpegWrap = `#!/bin/bash
args=(); for a in "$@"; do [[ "$a" == "libfdk_aac" ]] && a=aac; args+=("$a"); done
exec "${sysFfmpeg}" "\${args[@]}"
`;
fs.writeFileSync(path.join(dir, "ffmpeg"), ffmpegWrap);
fs.chmodSync(path.join(dir, "ffmpeg"), 0o755);
console.log("[duno-fix] ffmpeg wrapper installed (libfdk_aac → aac)");
