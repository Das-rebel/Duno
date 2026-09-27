# Duno R4 — one-shot rebuild. Clean clone → `make video` → full bundle.
VO_FILE   ?= public/voiceover.mp3
MUSIC_FILE ?= public/music.mp3
SCRIPT    ?= script.txt
VOICE     ?= en-US-GuyNeural
VARIANT   ?= slam
SCALE     ?= 1.0

MASTER := out/master.mp4

.PHONY: video vo render mix qa cuts score thumb clean

video: vo render mix qa cuts score thumb
	@echo "════ BUNDLE READY ════"; ls -lh out/

vo: $(VO_FILE)
	@test -f $(SCRIPT) || (echo "write your VO script to $(SCRIPT) first"; exit 1)
	bash ../../scripts/vo.sh $(SCRIPT) $(VOICE) public/
	@mv public/voiceover.mp3.bak $(VO_FILE) 2>/dev/null || true

$(VO_FILE):
	@test -f $@ || (echo "provide $(VO_FILE) or run: make vo SCRIPT=script.txt"; exit 1)

render: $(MASTER)

$(MASTER): src src/index.tsx
	npx remotion render src/index.tsx Video $(MASTER) \
	  --props='{"hookVariant":"$(VARIANT)"}' --codec h264 --crf 18 --scale=$(SCALE) --log=error

# sound-design pass: procedural SFX + ducked music (needs beats.json)
mix: render
	@test -f beats.json || (printf '[{"t":3.0,"sfx":"impact"}]\n' > beats.json && echo "wrote starter beats.json — edit it")
	bash ../../scripts/mix_master.sh $(MASTER) beats.json $(MUSIC_FILE) out/master-sfx.mp4

qa: render
	python3 ../../scripts/qa_video.py --video $(MASTER) --beats qa_beats.json

cuts: render
	bash ../../scripts/social_cuts.sh $(MASTER) out/

score:
	python3 ../../scripts/score.py

thumb:
	npx remotion still src/index.tsx Thumb out/thumb-raw.png --frame 140

clean:
	rm -rf out/*
