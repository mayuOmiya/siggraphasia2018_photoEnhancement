#!/bin/bash

date=$1
echo "$1"

python2 mv_thresholdedPhotos.py $date
python2 list_chosenPhotos.py $date