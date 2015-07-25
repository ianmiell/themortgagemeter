#!/bin/bash
IMAGE=$1
DOCKER=${DOCKER:-docker}
pushd ..
$DOCKER run -t -d -h themortgagemeter --name themortgagemeter -p 40001:80 $IMAGE /root/start_themortgagemeter.sh
popd
