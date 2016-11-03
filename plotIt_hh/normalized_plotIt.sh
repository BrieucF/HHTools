#! /bin/bash

plotDate=`date +%F`

if [ -z "$1" ]; then
    suffix=""
else
    suffix=_$1
fi

plotDir=plots_normalized_${plotDate}${suffix}

mkdir ${plotDir}

../../plotIt/plotIt -o ${plotDir} normalized_plotter.yml -y
