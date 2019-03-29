#!/bin/bash

date=$1
echo "$1"

FILENAME_1="flickr-data/"
FILENAME_2="/temp_file_name.txt"
FILENAME=$FILENAME_1$date$FILENAME_2

mkdir -p "flickr-data/estimated_images"
mkdir -p "flickr-data/estimated_images/log"

for i in $(cat $FILENAME); do
	echo $i
	python CMAes-estimate-flickr.py $i > "flickr-data/estimated_images/log/log_"$i".txt"
done
