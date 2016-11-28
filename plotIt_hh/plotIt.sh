#! /bin/bash

plotDate=`date +%F`

if [ -z "$1" ]; then
    prefix=""
else
    prefix=$1
fi

plotDir=${prefix}_plots_all_${plotDate}

mkdir ${plotDir}

../../plotIt/plotIt -o ${plotDir} hh_plotter_all.yml -y
