#!/bin/bash

date=$1
echo "$1"

FILENAME_1="flickr-data/"
FILENAME_2="/all_chosen_degraded_file_name.txt"
FILENAME=$FILENAME_1$1$FILENAME_2

mkdir -p "flickr-data/estimated_images/evaluate"

for i in $(cat $FILENAME); do
	echo "$i" 
	python2 evaluate4losses.py $i > /dev/null 2>&1
done