# Learning Photo Enhancement by Black-Box Model Optimization Data Generation
Mayu Omiya, Edgar Simo-Serra, Satoshi Iizuka, Hiroshi Ishikawa


## Overview
This code provides an implementation of the research paper:

	"Learning Photo Enhancement by Black-Box Model Optimization Data Generation"
	Mayu Omiya, Edgar Simo-Serra, Satoshi Iizuka, Hiroshi Ishikawa
  	SIGGRAPH Asia 2018 technical brief

We address the problem of automatic photo enhancement, in which the challenge is to determine the optimal enhancement for a given photo according to its content. We propose generating supervised training data from high-quality professional images and train CNN.

![sample-input](https://user-images.githubusercontent.com/48705918/55223421-8218c200-5251-11e9-8c80-bcf8bb48a101.jpg)
![sample-output](https://user-images.githubusercontent.com/48705918/55223422-8218c200-5251-11e9-86d1-9067887cd848.jpg)

## Dependencies
- pytorch
- Image
- cma
- darktable(Photo enhancement software)

## Contents
This contains programs for generating training data and ones for using trained CNN to enhance photos.
