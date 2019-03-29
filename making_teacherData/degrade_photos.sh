#!/bin/bash

date=$1
echo "$1"

python2 randomely_degrade_photos.py $date
python2 list_degradedPhotos.py $date

