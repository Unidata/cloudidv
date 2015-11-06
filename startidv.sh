#!/bin/bash

###
# This script does several things:
#
# 1. Starts up the X session in a virtual framebuffer; password
#    use is dictated by value of USEPASS environmental variable.
# 2. Launches the IDV, using the VFB as the display.
#
# This is necessary to do here; if we put the xinit command
# in the Dockerfile, it would not run if we invoke this script
# from the 'docker run' command.  If we put the IDV in .xinitrc,
# then it would cause problems for those downstream images that
# don't want to automatically run the IDV.
#
# Therefore, we must run a command that starts xinit and then
# runs the IDV.  Other images will need to do something similar.
#
# This has the added benefit of killing the image when the IDV exits.
###

set -e

trap "echo TRAPed signal" HUP INT QUIT KILL TERM

if [ "x${HELP}" != "x" ]; then
    cat README.md
    exit
fi

if [ "x${USEPASS}" == "x" ]; then
    cp /home/idv/.xinitrc.nopassword /home/idv/.xinitrc
else
    mkdir -p /home/idv/.vnc
    cp /home/idv/.xinitrc.password /home/idv/.xinitrc
    x11vnc -storepasswd "${USEPASS}" /home/idv/.vnc/passwd
fi

xinit -- /usr/bin/Xvfb :1 -screen 0 $SIZEH\x$SIZEW\x$CDEPTH &
sleep 5

export DISPLAY=localhost:1

pushd /home/idv/noVNC/utils/
openssl req -new -x509 -days 365 -nodes -out self.pem -keyout self.pem -passout pass:foobar -subj "/C=US/ST=ANY/L=Anytown/O=Dis/CN=thishost.local"
popd
/home/idv/noVNC/utils/launch.sh --vnc 127.0.0.1:${APORT} &
