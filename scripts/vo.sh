#!/usr/bin/env bash
# Duno VO: script → voiceover.mp3 + whisper timing map
# usage: vo.sh script.txt [voice] [out_dir]
set -euo pipefail
SCRIPT="${1:?usage: vo.sh script.txt [voice] [out_dir]}"
VOICE="${2:-en-US-GuyNeural}"
OUT="${3:-.}"
mkdir -p "$OUT"
python3 -m edge_tts --voice "$VOICE" --rate=-4% --text "$(cat "$SCRIPT")" \
  --write-media "$OUT/voiceover.mp3"
echo "VO: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/voiceover.mp3")s"
python3 - "$OUT/voiceover.mp3" << 'PYEOF'
import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(sys.argv[1], language="en", vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=400), word_timestamps=True)
out = []
for s in segs:
    print(f"  [{s.start:6.2f} - {s.end:6.2f}]  {s.text.strip()}")
    out.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
open(sys.argv[1].rsplit("/", 1)[0] + "/timing.json", "w").write(json.dumps(out, indent=1))
print("→ timing.json written (scene boundaries go in the gaps)")
PYEOF
