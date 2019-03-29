# Learning Photo Enhancement by Black-Box Model Optimization Data Generation
Mayu Omiya, Edgar Simo-Serra, Satoshi Iizuka, Hiroshi Ishikawa


## Overview
This code provides an implementation of the research paper:

	"Learning Photo Enhancement by Black-Box Model Optimization Data Generation"
	Mayu Omiya, Edgar Simo-Serra, Satoshi Iizuka, Hiroshi Ishikawa
  	SIGGRAPH Asia 2018 technical brief

We address the problem of automatic photo enhancement, in which the challenge is to determine the optimal enhancement for a given photo according to its content. We propose generating supervised training data from high-quality professional images and train CNN.

See our [project page](http://hi.cs.waseda.ac.jp/index.php/ja/%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E4%B8%80%E8%A6%A7/%E7%94%BB%E5%83%8F%E7%B7%A8%E9%9B%86/77-%E7%9F%B3%E5%B7%9D%E7%A0%94/91-omiya_photoenhance_en) or [paper](https://waseda.box.com/s/vbs0btql52r7wi7l4zalbgva7c29qhk4) for more detailed information.



![sample-input](https://user-images.githubusercontent.com/48705918/55223421-8218c200-5251-11e9-8c80-bcf8bb48a101.jpg)
![sample-output](https://user-images.githubusercontent.com/48705918/55223422-8218c200-5251-11e9-86d1-9067887cd848.jpg)

## Dependencies
- pytorch
- Image
- cma
- darktable (Photo enhancement software)

## Contents
This contains programs for generating training data and ones for using trained CNN to enhance photos.
