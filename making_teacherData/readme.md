# Generating training data
These are programs for generating training data.

## Usage 
First, download the high-quality images from flickr. Be sure to enter your flicker API key.

	python2 flickrAPI.py 2019-01-31

Second, degrade images and choose natural ones from them.

	bash degrade_photos.sh 2019-01-31
	python choose_degraded_photos-test.py test --datedir 2019-01-31
	python thresholding.py　 2019-01-31
	bash choose_degraded_photos.sh 2019-01-31

Finally, the optimization calculation is performed to restore the degraded image to the original high-quality image. The enhancement parameters obtained by the optimization and the degraded images become the training data.

	bash makeDatasetCMA.sh 2019-01-31
	bash evaluate.sh
	bash thresholding.sh 2019-01-31
