#!/bin/bash
IMAGE=$1
pushd ..
DOCKER=${DOCKER:-docker.io}
$DOCKER run -t -d -h themortgagemeter --name themortgagemeter -p 40001:80 $IMAGE /root/start_themortgagemeter.sh
popd
