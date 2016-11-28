#! /bin/bash

plotDate=`date +%F`

if [ -z "$1" ]; then
    prefix=""
else
    prefix=$1
fi

plotDir=${prefix}_plots_normalized_${plotDate}

mkdir ${plotDir}

../../plotIt/plotIt -o ${plotDir} normalized_plotter.yml -y
