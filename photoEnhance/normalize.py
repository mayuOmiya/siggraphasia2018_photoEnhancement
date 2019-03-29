import numpy as np
import pandas as pd


def paramReader(paramfileName):
	f = open(paramfileName, 'r')
	for input_string in f:
		if input_string.split(' ')[0]=='exposure':
			exposure_black = input_string.split(' ')[2]
			exposure_exposure = input_string.split(' ')[3]
		if input_string.split(' ')[0]=='shadhi':
			shadhi_shadow = input_string.split(' ')[2]
			shadhi_whitepoint = input_string.split(' ')[3]
			shadhi_highlight = input_string.split(' ')[4]
			shadhi_shadowSat = input_string.split(' ')[5]
			shadhi_highlightSat = input_string.split(' ')[6]
		if input_string.split(' ')[0]=='colisa':
			colisa_contrast = input_string.split(' ')[2]
			colisa_light = input_string.split(' ')[3]
			colisa_saturation = input_string.split(' ')[4]
		if input_string.split(' ')[0]=='temperature':
			temperature_red = input_string.split(' ')[2]
			temperature_green = input_string.split(' ')[3]
			temperature_blue = input_string.split(' ')[4]
		if input_string.split(' ')[0]=='vibrance':
			vibrance_vibrance = input_string.split(' ')[2]
		if input_string.split(' ')[0]=='colorcorrection':
			colorcorrection_highX = input_string.split(' ')[2]
			colorcorrection_highY = input_string.split(' ')[3]
			colorcorrection_shadX = input_string.split(' ')[4]
			colorcorrection_shadY = input_string.split(' ')[5]
			colorcorrection_saturation = input_string.split(' ')[6]
		if input_string.split(' ')[0]=='colorcontrast':
			colorcontrast_GM = input_string.split(' ')[2]
			colorcontrast_BY = input_string.split(' ')[3]
	f.close()
	return np.array([ exposure_black, exposure_exposure, shadhi_shadow, shadhi_whitepoint, shadhi_highlight, shadhi_shadowSat, shadhi_highlightSat, colisa_contrast, colisa_light, colisa_saturation, temperature_red, temperature_green, temperature_blue, vibrance_vibrance, colorcorrection_highX, colorcorrection_highY, colorcorrection_shadX, colorcorrection_shadY, colorcorrection_saturation, colorcontrast_GM, colorcontrast_BY ]).astype(np.float64).astype(np.float64)

def normalize(param): #normalize parameter value by train data

	#calculate mean, std by calc_MeanStd_params.py
	"""
	#0319 flickr-parameters_2017-10-27_2017-12-14-train.csv
	mean = np.array([  0.00139, 0.02395, 67.13252, -0.10759, -69.29769, 100.00000, 50.55960,
					 0.07488, -0.10928, 0.03422, 1.08851, 1.11449, 1.08056, 14.16835, -0.10907,
					 0.09209, 0.31035, 1.28927, 0.87302, 0.90572, 1.08901 ])

	std = np.array([ 0.05683, 1.01130, 38.94620, 5.95787, 37.79219, 0.000001, 32.29216, 0.40924,
				 0.45745, 0.47732, 0.47473, 0.48634, 0.49259, 20.60017, 13.07512, 13.67016,
				  12.76837, 12.81461, 0.69919, 0.47395, 0.51750])
	"""
	#2016-09_2017-12
	mean = np.array([ 0.00019, 0.00038, 51.68072, 0.00026, -53.04044, 73.35190, 52.01958, 0.00024, 0.00041, 0.47265, 0.96978, 0.94532, 0.93164, 26.38616, 0.00020, 0.00017, 0.00016, 0.00022, 0.75903, 0.82752, 1.03499 ])
	std = np.array([ 0.00397, 0.00260, 32.87102, 0.00269, 25.69292, 23.77706, 18.15760, 0.00263, 0.00367, 0.20749, 0.50417, 0.47204, 0.51336, 10.91563,	0.00263, 0.00258, 0.00269, 0.00274, 0.42436, 0.41313, 0.44567 ])
	#mean = np.array([ 0.00019, 0.00038, 51.68072, 0.00026, 53.04044, 73.35190, 52.01958, 0.00024, 0.00041, 0.47265, 0.96978, 0.94532, 0.93164, 26.38616, 0.00020, 0.00017, 0.00016, 0.00022, 0.75903, 0.82752, 1.03499 ])
	#std = np.array([ 0.00397, 0.00260, 32.87102, 0.00269, 25.69292, 23.77706, 18.15760, 0.00263, 0.00367, 0.20749, 0.50417, 0.47204, 0.51336, 10.91563, 0.00263, 0.00258, 0.00269, 0.00274, 0.42436, 0.41313, 0.44567 ])
	return (param - mean)/std

def denormalize(normalized_param): #denormalize parameter value by train data

	mean = np.array([ 0.00019, 0.00038, 51.68072, 0.00026, -53.04044, 73.35190, 52.01958, 0.00024, 0.00041, 0.47265, 0.96978, 0.94532, 0.93164, 26.38616,	0.00020, 0.00017, 0.00016, 0.00022, 0.75903, 0.82752, 1.03499 ])
	std = np.array([ 0.00397, 0.00260, 32.87102, 0.00269, 25.69292, 23.77706, 18.15760, 0.00263, 0.00367, 0.20749, 0.50417, 0.47204, 0.51336, 10.91563,	0.00263, 0.00258, 0.00269, 0.00274, 0.42436, 0.41313, 0.44567 ])
	#mean = np.array([ 0.00019, 0.00038, 51.68072, 0.00026, 53.04044, 73.35190, 52.01958, 0.00024, 0.00041, 0.47265, 0.96978, 0.94532, 0.93164, 26.38616, 0.00020, 0.00017, 0.00016, 0.00022, 0.75903, 0.82752, 1.03499 ])
	#std = np.array([ 0.00397, 0.00260, 32.87102, 0.00269, 25.69292, 23.77706, 18.15760, 0.00263, 0.00367, 0.20749, 0.50417, 0.47204, 0.51336, 10.91563, 0.00263, 0.00258, 0.00269, 0.00274, 0.42436, 0.41313, 0.44567 ])
	return std*normalized_param + mean

if __name__ == '__main__':


	param = paramReader('/home/omiya/data/NelderMead_Dataset/a0001to0700/parameters/a0002_parameter_nm.txt')
	
	normalized_param = normalize(param)
	denormalized_param = denormalize(normalized_param)
	
	print (normalized_param)
	