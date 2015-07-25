#!/bin/bash
pushd ..
shutit build --shutit_module_path $(dirname $(which shutit))/../shutit-library --image_tag ubuntu:14.04.2
if [[ "x$?" != "x0" ]]
then
	popd
	exit 1
fi
popd
