# Learning Photo Enhancement by Black-Box Model Optimization Data Generation
Mayu Omiya, Edgar Simo-Serra, Satoshi Iizuka, Hiroshi Ishikawa


## Overview
This code provides an implementation of the research paper:

	"Learning Photo Enhancement by Black-Box Model Optimization Data Generation"
	Mayu Omiya, Edgar Simo-Serra, Satoshi Iizuka, Hiroshi Ishikawa
  	SIGGRAPH Asia 2018 technical brief

We address the problem of automatic photo enhancement, in which the challenge is to determine the optimal enhancement for a given photo according to its content. We propose generating supervised training data from high-quality professional images and train CNN.

![sample-input](https://user-images.githubusercontent.com/48705918/55223027-a2944c80-5250-11e9-97a9-42f00b62e7e9.JPG)
![sample-output](https://user-images.githubusercontent.com/48705918/55223036-a6c06a00-5250-11e9-9cd8-856297081b71.jpg)

## Dependencies
- pytorch
- Image
- cma
- darktable(Photo enhancement software)

## Contents
This contains programs for generating training data and ones for using trained CNN to enhance photos.
