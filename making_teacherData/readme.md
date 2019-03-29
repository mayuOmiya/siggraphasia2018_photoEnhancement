# Generating training data
These are programs for generating training data.

## Usage 
First, download the high-quality images from flickr. Be sure to enter your flicker API key.

	python2 flickrAPI.py ''date (ex. 2019-01-31)''

Second, degrade images and choose natural ones from them.

Download the [classification net](https://waseda.box.com/s/bq9oy7ep8utfybn8007dw55amtsiumxh).

	bash degrade_photos.sh ''date''
	python choose_degraded_photos-test.py test --datedir ''date''
	python thresholding.py　 ''date''
	bash choose_degraded_photos.sh ''date''

Finally, the optimization calculation is performed to restore the degraded image to the original high-quality image. The enhancement parameters obtained by the optimization and the degraded images become the training data.

	bash makeDatasetCMA.sh ''date''
	bash evaluate.sh ''date''
	bash thresholding.sh ''date''
