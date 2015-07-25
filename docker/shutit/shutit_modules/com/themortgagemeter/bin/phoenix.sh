#!/bin/bash
./build.sh
DOCKER=${DOCKER:-docker}
# Kill the name of the container.
$DOCKER rm -f themortgagemeter
./run.sh themortgagemeter/themortgagemeter

