# Build tutorial video

`Clown-Build-Tutorial.mp4` in the repo root — 35:18, 1920x1080, narrated.
Generated, not hand-edited, the same way the PDF manual is.

- `deck.py` — every slide and every line of narration. Edit this.
- `render.py` — draws the slides (Pillow) and speaks the narration (macOS `say`),
  then writes `manifest.json`, `tutorial.srt` and `chapters.txt`.
- `Assemble.swift` — muxes slides + narration into the MP4 via AVFoundation.
  No ffmpeg needed; everything used here ships with macOS.

## Regenerating

```
cd docs/tutorial
python3 render.py                 # slides + narration + manifest
swiftc -O -o assemble Assemble.swift
./assemble manifest.json ../../Clown-Build-Tutorial.mp4
```

Delete `audio/` first if you changed narration text — cached clips are reused.

## Notes

- Voice is macOS `Samantha` at rate 174. Change in `render.py:narrate()`.
- Slide timing is derived from narration length, so edits re-time automatically.
- `tutorial.srt` is burned from the same text — load it as a sidebar subtitle track.
- Numbers, pin tables and warnings are transcribed from BUILD.md. If a step
  changes there, change it in `deck.py` too.
- **Part and pin names must follow the [naming rules](../../SCHEMATIC.md#naming-rules).**
  Diodes are `CR1`/`CR2`, XIAO pins are GPIO numbers, and the silkscreen
  D-numbers appear only in the pin-table column that is labelled as such. This
  applies to the spoken narration as well as the slide text — the narration is
  the only place a viewer hears a name, so "C R two" and "G P I O four" are what
  it has to say.
