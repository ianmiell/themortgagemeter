#!/bin/bash
./build.sh
# Kill the name of the container.
DOCKER=${DOCKER:-docker}
$DOCKER rm -f themortgagemeter
./run.sh themortgagemeter/themortgagemeter

