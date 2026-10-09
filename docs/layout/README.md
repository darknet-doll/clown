# Pod perfboard layouts

Step-by-step build of the controller pod on a 3 × 7 cm perfboard. Each file is a
self-contained page: open it in a browser, step through the build, and flip the
board between the Top and Bottom views.

| File | What it is | Published copy |
|---|---|---|
| [pod-layout-v2.html](pod-layout-v2.html) | **Current.** Steps 1–34 match v1. From step 35 on, the steps run in three passes: jumpers soldered at both ends, then jumpers that leave an end parked, then off-board wires. Tracks parked ends. The Bottom view uses the back silkscreen's letters | [V2 Pod Layout](https://claude.ai/artifact/KwUK4EnDZno9KLW17SxdUp) |
| [pod-layout-v1.html](pod-layout-v1.html) | The original order, kept for reference. Already has `J2`/`J3` on the edge pads | [Pod Layout](https://claude.ai/artifact/U9Gy8j4RQ4VKG7HhV2fXmE) |

- **Hole names are front-side.** Columns A–X, rows 1–10. Y2–Y9 are the oblong
  edge pads past column X, at the harness end; "Y" isn't printed on the board.
- **The back silkscreen runs the letters the other way:** front A = back X.
- **The repo copy and the published copy are edited separately.** After changing
  one, update the other so they stay the same.
- **Everything is in the HTML.** The parts, holes, wires and step order are data
  arrays (`holes`, `WIRES`, `ADDS`, `PARKED`) in the script at the bottom of each
  file. The step text is the Build Order table.
