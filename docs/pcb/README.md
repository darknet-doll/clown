# Pod PCB

The pod circuit from the [perfboard layout](../layout/README.md) as a real
two-layer board. Same parts, same nets and same designators as
[SCHEMATIC.md](../../SCHEMATIC.md). Everything is through-hole and hand-soldered.

![Top](fab/clown-pod-top.png)

| File | What it is |
|---|---|
| [fab/clown-pod-gerbers.zip](fab/clown-pod-gerbers.zip) | **The upload for PCBWay.** Gerbers for copper, mask, silk and outline, plus Excellon drill files |
| [clown-pod.kicad_pcb](clown-pod.kicad_pcb) | The board, opens in KiCad 9 |
| [pod_pcb.py](pod_pcb.py) | The source: outline, placement, netlist, silkscreen |
| [build.sh](build.sh) | Rebuilds everything: place, autoroute, ground pour, DRC, export |

## Ordering on PCBWay

Upload `fab/clown-pod-gerbers.zip` as a standard PCB. The board size and layer
count come from the files. Every other setting is PCBWay's default:

| Setting | Value |
|---|---|
| Size | 70 × 30 mm |
| Layers | 2 |
| Material / thickness | FR-4, 1.6 mm |
| Copper | 1 oz |
| Min track / spacing | 0.3 mm / 0.25 mm. That's 12/10 mil, well inside the standard 6/6 mil |
| Min hole | 0.6 mm (the two vias). The smallest part hole is 0.8 mm |
| Surface finish | HASL lead-free |
| Quantity | 5, the minimum. One board per arm leaves three spares |

Order the bare board only. No assembly, no stencil: the parts are already in
hand (see [PARTS.md](../../PARTS.md)).

## The board

- **70 × 30 mm, an M2 hole 2.5 mm in from each corner.** It's the size of the
  3 × 7 cm perfboard it replaces. Check the hole positions against the pod
  cradle before printing it
- **U3 (XIAO) sits on two 7-pin headers, USB-C hanging off the left edge**, so
  a cable reaches it through the pod wall. Pin 1 (`U3 GPIO2`) is the square pad.
  Pin 14 (`U3 5V`) is directly across from it
- **U2 is a DIP-14 socket footprint.** Fit a socket or solder the chip
- **Off-board parts land on wire pads.** These are `U1` (the MT3608 module,
  `IN+ IN− OUT+ OUT−`), `SW1`, `J1` (the cell's PH2.0 lead), `J2` (strip SM-3)
  and `J3` (elbow SM-4). Pad 1 of each is square. J2 and J3 pad labels give the
  pin and its job
- **Power nets** (cell, motor, +5 V, ground) run at 0.8 mm, signals at 0.3 mm.
  Both layers carry a ground pour. Q1's source is tied solid to the pour, with
  no thermal spokes
- **Polarity on the silkscreen.** `CR2` has its band toward the XIAO, marked
  `K`. `C1` has its `+` beside the square pad

Four short net stretches get names here that the schematic draws but doesn't
name. `VBATT_RAW` is `J1-1` to `SW1`, and `VBATT_SW` is `SW1` to `F1`.
`GATE_Q` is `R4` to `Q1 G` and `R5`. `LED_DATA_STRIP` is `R3` to `J2-3`.

## Rebuilding

```
docs/pcb/build.sh
```

Needs Docker and Java 17+. KiCad 9 runs from the `kicad/kicad:9.0.4` image, and
Freerouting 2.1.0 is downloaded to `~/.cache/freerouting` the first time. The
script stops if DRC finds any error or unconnected pad. `build/` holds
intermediates and is ignored. Edit `pod_pcb.py`, never the `.kicad_pcb`: the
board is regenerated from scratch on every run.
