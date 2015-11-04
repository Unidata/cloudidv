#!/bin/bash
#
# Convienence script to launch a docker container version of the IDV with all of the appropriate arguments.

if [ $# -lt 1 ]; then
    docker images
    echo ""
    echo "You must specify a docker image."
    exit 1
fi

set -x

docker run -p 5901:5901 --rm -it $1 /home/idv/startidv.sh
