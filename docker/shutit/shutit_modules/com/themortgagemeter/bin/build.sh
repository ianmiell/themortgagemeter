#!/bin/bash
pushd ..
${SHUTITDIR}/shutit build --shutit_module_path ${SHUTITDIR}/library --image_tag stackbrew/ubuntu:saucy
popd
