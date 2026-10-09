#!/bin/bash
# Build the pod PCB and the PCBWay upload. Needs Docker and Java 17+.
#
#   docs/pcb/build.sh
#
# 1. place    - KiCad 9 (Docker): outline, parts, nets -> .kicad_pcb + .dsn
# 2. route    - Freerouting (host Java): .dsn -> .ses
# 3. finish   - KiCad 9: import the routing, pour ground
# 4. check    - kicad-cli DRC; stops on any error or unconnected item
# 5. export   - Gerbers + drill -> fab/clown-pod-gerbers.zip, plus renders
set -euo pipefail
cd "$(dirname "$0")"

KICAD_IMAGE=kicad/kicad:9.0.4
FR_VERSION=2.1.0
FR_JAR="${XDG_CACHE_HOME:-$HOME/.cache}/freerouting/freerouting-$FR_VERSION.jar"

kicad() {
  docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -v "$PWD:/work" -w /work "$KICAD_IMAGE" "$@"
}

if [ ! -f "$FR_JAR" ]; then
  mkdir -p "$(dirname "$FR_JAR")"
  curl -fsSL -o "$FR_JAR" \
    "https://github.com/freerouting/freerouting/releases/download/v$FR_VERSION/freerouting-$FR_VERSION.jar"
fi

mkdir -p build fab
kicad python3 pod_pcb.py place
rm -f build/clown-pod.ses
java -jar "$FR_JAR" -de build/clown-pod.dsn -do build/clown-pod.ses -mp 100 -mt 1 \
  -inc gnd \
  --gui.enabled=false >build/freerouting.log 2>&1 || true
[ -f build/clown-pod.ses ] || { tail -30 build/freerouting.log; exit 1; }
kicad python3 pod_pcb.py finish

kicad kicad-cli pcb drc --severity-error --exit-code-violations \
  -o build/drc.rpt clown-pod.kicad_pcb \
  || { cat build/drc.rpt; exit 1; }

rm -rf build/gerbers && mkdir -p build/gerbers
kicad kicad-cli pcb export gerbers --no-protel-ext \
  --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts \
  -o build/gerbers/ clown-pod.kicad_pcb
kicad kicad-cli pcb export drill --format excellon --excellon-separate-th -o build/gerbers/ clown-pod.kicad_pcb
rm -f fab/clown-pod-gerbers.zip
(cd build/gerbers && zip -q ../../fab/clown-pod-gerbers.zip ./*)

kicad kicad-cli pcb render --side top --quality high --zoom 2.1 -w 1600 -h 760 \
  --background opaque -o fab/clown-pod-top.png clown-pod.kicad_pcb
kicad kicad-cli pcb render --side bottom --quality high --zoom 2.1 -w 1600 -h 760 \
  --background opaque -o fab/clown-pod-bottom.png clown-pod.kicad_pcb
echo "done: fab/clown-pod-gerbers.zip"
