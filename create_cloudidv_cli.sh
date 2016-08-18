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
# Spawn an instance
#
# Input: name, port, password
###
spawnidv() {

    HNAME=$1
    PORT=$2
    PWORD=$3
    IMEM=$4

    ##
    # Remove extant named machine if it exists.
    ##
    echo "Checking if $HNAME exists, skipping if so."
    set +e
    if [ $(docker ps -a | grep $HNAME | wc -l | tr -s " " | cut -d " " -f 2 ) -gt 0 ]; then
       echo "$HNAME Found."

       return 0
    fi
    set -e
    ###
    # Make sure data volume is there.
    ###
    DVOL=$(pwd)/datavols/$HNAME
    if [ ! -d "$DVOL" ]; then
        mkdir -p $DVOL
    fi

    echo "Processing $HNAME $PORT $PWORD $IMEM"

    # docker run -d -it --hostname $HNAME --name $HNAME -p $PORT:6080 -e PASS=$PWORD -v $DVOL:/home/stream/.unidata -e SSLONLY=TRUE unidata/cloudidv
    docker run -d -it --hostname $HNAME --name $HNAME -p $PORT:6080 -e USEPASS=$PWORD -e SSLONLY=TRUE -e IDVMEM=$IMEM -e SHARED=TRUE unidata/cloudidv

}

###
# Print out the help dialog.
###
dohelp() {

    echo -e ""
    echo "Usage: $0 [instance name] [port] [password] [memory in MB] -f <filename>"
    echo ""
    echo -e "  * [instance name]:\tThis will also be used for the hostname"
    echo -e "                    \tand the data directory mapping."
    echo -e "  * [port]:\t\tThe external port to expose for connections."
    echo -e "  * [password]:\t\tThe session must be password protected."
     echo -e "  * <filename>:\t\tYou may alternatively construct a SPACE-delimited file containing this information and pass it with the -f switch."
   echo -e ""
    echo -e "Example:"
    echo -e ""
    echo -e "\t$ $0 test1 6080 abcd1234"
    echo -e "\t$ $0 -f machines.txt"
    echo -e ""
}

INFILE=""

while getopts "f:" o; do
    case "${o}" in
        f)
            INFILE=${OPTARG}
            ;;
        *)
            dohelp
            exit 0
            ;;
    esac
done




if [ "x$INFILE" == "x" ]; then

    if [ $# -ne 4 ]; then
        echo ""
        echo "Wrong number of arguments!"
        echo ""
        dohelp
        exit 1
    fi

    HNAME=$1
    PORT=$2
    PASS=$3
    IMEM=$4

    ##
    # Run the instance detached
    ##
    spawnidv $HNAME $PORT $PASS $IMEM


else # Reading in from a file

    if [ ! -f $INFILE ]; then
        echo "Error reading $INFILE."
        exit 1
    fi

    echo "Reading configuration in from file: $INFILE"

    while read HNAME PORT PASS IMEM
    do

        spawnidv $HNAME $PORT $PASS $IMEM
        sleep 1

    done < $INFILE

fi





echo "Finished"
