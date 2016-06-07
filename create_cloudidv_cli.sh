#!/bin/bash

set -e

########################################
# Copyright 2016 Unidata
#
# This is a utility script for creating a
# CloudIDV instance from the command line.
# It doesn't do anything you can't do with
# the docker-cli, but it is simplified.
########################################

########################################
# Input:
#
# HostName/InstanceName (these will be the same)
# Password to use for authentication
# Port to open on.
#
# The script will mount the .unidata directory from
# the docker container into $(pwd)/docker-volumes/$docker-hostname
########################################

###
# Print out the help dialog.
###
dohelp() {

    echo -e ""
    echo "Usage: $0 [instance name] [port] [password]"
    echo ""
    echo -e "  * [instance name]:\tThis will also be used for the hostname"
    echo -e "                    \tand the data directory mapping."
    echo -e "  * [port]:\t\tThe external port to expose for connections."
    echo -e "  * [password]:\t\tThe session must be password protected."
    echo -e ""
    echo -e "Example:"
    echo -e ""
    echo -e "\t$ $0 test1 6080 abcd1234"
    echo -e ""
}

if [ $# -ne 3 ]; then
    echo ""
    echo "Wrong number of arguments!"
    echo ""
    dohelp
    exit 1
fi




echo "Finished"
