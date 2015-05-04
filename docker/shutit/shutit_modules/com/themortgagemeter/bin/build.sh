#!/bin/bash
pushd ..
shutit build --shutit_module_path $(dirname $(which shutit))/library --image_tag ubuntu:14.04.2 --interactive 0
if [[ "x$?" != "x0" ]]
then
	popd
	exit 1
fi
popd
