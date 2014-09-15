#!/bin/bash
./build.sh
# Kill the name of the container.
$DOCKER rm -f themortgagemeter
./run.sh themortgagemeter/themortgagemeter

