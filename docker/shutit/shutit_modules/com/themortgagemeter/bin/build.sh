#!/bin/bash
pushd ..
shutit build --shutit_module_path $(dirname $(which shutit))/library --image_tag stackbrew/ubuntu:saucy --interactive 0
if [[ "x$?" != "x0" ]]
then
	popd
	exit 1
fi
popd
