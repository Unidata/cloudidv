#!/bin/bash

###
# This script is invoked by the `bootstrap.sh` script in the
# base unidata/cloudstream image.
###
sleep 10
if [ "x$USERCLONE" != "x" ]; then
    xterm -e "~/rclone-gui.py"
else
    ~/idv-launcher.py
fi
