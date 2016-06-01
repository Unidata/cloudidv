#!/bin/bash

###
# This script is invoked by the `bootstrap.sh` script in the
# base unidata/cloudstream image.
###

if [ "x$USERCLONE" != "x" ]; then
    xterm -e "~/rclone-gui.py"
else
    ~/IDV/runIDV
fi
