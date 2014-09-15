IMAGE=$1
pushd ..
$DOCKER run -t -d -h themortgagemeter --name themortgagemeter -p 40000:22 -p 40001:80 $IMAGE /root/start_themortgagemeter.sh
popd
