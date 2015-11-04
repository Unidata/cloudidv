#!/bin/bash

docker build -t unidata/idv-base -f Dockerfile.base .
docker build -t unidata/idv-gui -f Dockerfile.gui .
docker build -t unidata/cloudidv -f Dockerfile.gui .
