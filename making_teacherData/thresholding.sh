#!/bin/bash

date=$1
echo "$1"

#FILENAME_x="all_file_name.txt"
#FILENAME_1="/home/omiya/data/Flickr_Interestingness1109/original_photos/"
FILENAME_1="flickr-data/"
FILENAME_2="/all_chosen_degraded_file_name.txt"
FILENAME=$FILENAME_1$1$FILENAME_2

mkdir -p "datasets"
mkdir -p "datasets/input_images/"
mkdir -p "datasets/degrade_parameters/"
mkdir -p "datasets/original_images/" 
mkdir -p "datasets/target/estimated_parameters/"
mkdir -p "datasets/target/estimated_images/"


for i in $(cat $FILENAME); do
	#echo "$i" 
	python thresholding_datasets.py $i > /dev/null 2>&1
done

python list_datasets.py $date > /dev/null 2>&1