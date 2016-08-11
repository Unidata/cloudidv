#!/bin/bash

###
# This script is invoked by the `bootstrap.sh` script in the
# base unidata/cloudstream image.
###

if [ "x$USERCLONE" != "x" ]; then
    xterm -e "~/rclone-gui.py"
else
    
    ~/IDV/jre/bin/java -Xmx512m -XX:+DisableExplicitGC -Didv.enableStereo=false -jar ~/IDV/idv.jar 
    #~/IDV/runIDV
fi
