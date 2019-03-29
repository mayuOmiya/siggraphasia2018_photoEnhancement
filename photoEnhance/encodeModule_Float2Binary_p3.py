import sys
import struct
import binascii
import re

def float_to_binary_string(floatValue):
	binStr = binascii.b2a_hex( struct.pack("f", floatValue) )
	#print floatValue, '->', binStr
	#binStr2 = [(i+j) for (i,j) in zip(binStr[::2],binStr[1::2])]
	return binStr


#print 'float -> binary string\n'

def encode_f2b(paramfile_name, XMPdataFile_name):
	
	f = open(paramfile_name, 'r')


	for input_string in f:

		"""
		if input_value=='q\n':
			break
		"""

		if input_string.split(' ')[0]=='exposure':
			exposure_black = input_string.split(' ')[2]
			exposure_exposure = input_string.split(' ')[3]

			#print '\nexposure'

			#print ' black: ', exposure_black
			#binaryParam_black = float_to_binary_string( float(exposure_black) )
			binaryParam_black = re.split( "[']", str(float_to_binary_string( float(exposure_black) )) )[1]
			#print ' exposure: ', exposure_exposure
			#binaryParam_exposure = float_to_binary_string( float(exposure_exposure) )
			binaryParam_exposure = re.split( "[']", str(float_to_binary_string( float(exposure_exposure) )) )[1]

			exposure = '00000000'+binaryParam_black+binaryParam_exposure+'00004842000080c0'
			
			#print 'exposure ', exposure
		

		if input_string.split(' ')[0]=='shadhi':
			shadhi_shadow = input_string.split(' ')[2]
			shadhi_whitepoint = input_string.split(' ')[3]
			shadhi_highlight = input_string.split(' ')[4]
			shadhi_shadowSat = input_string.split(' ')[5]
			shadhi_highlightSat = input_string.split(' ')[6]

			#binaryParam_shadow = float_to_binary_string( float(shadhi_shadow) )
			binaryParam_shadow = re.split( "[']", str(float_to_binary_string( float(shadhi_shadow) )) )[1]
			binaryParam_whitepoint = re.split( "[']", str(float_to_binary_string( float(shadhi_whitepoint) )) )[1]
			binaryParam_highlight = re.split( "[']", str(float_to_binary_string( float(shadhi_highlight) )) )[1]
			binaryParam_shadowSat = re.split( "[']", str(float_to_binary_string( float(shadhi_shadowSat) )) )[1]
			binaryParam_highlightSat = re.split( "[']", str(float_to_binary_string( float(shadhi_highlightSat) )) )[1]
			
			shadhi = '000000000000c842'+binaryParam_shadow+binaryParam_whitepoint+binaryParam_highlight+'0000000000004842'+binaryParam_shadowSat+binaryParam_highlightSat+'7f000000bd37863500000000'
			
			#print 'shadhi ', shadhi

		if input_string.split(' ')[0]=='colisa':
			colisa_contrast = input_string.split(' ')[2]
			colisa_light = input_string.split(' ')[3]
			colisa_saturation = input_string.split(' ')[4]
			
			binaryParam_contrast = re.split( "[']", str(float_to_binary_string( float(colisa_contrast) )) )[1]
			binaryParam_light = re.split( "[']", str(float_to_binary_string( float(colisa_light) )) )[1]
			binaryParam_saturation = re.split( "[']", str(float_to_binary_string( float(colisa_saturation) )) )[1]
			
			colisa = binaryParam_contrast+binaryParam_light+binaryParam_saturation

			#print 'colisa ', colisa

		if input_string.split(' ')[0]=='temperature':
			temperature_red = input_string.split(' ')[2]
			temperature_green = input_string.split(' ')[3]
			temperature_blue = input_string.split(' ')[4]
			
			binaryParam_red = re.split( "[']", str(float_to_binary_string( float(temperature_red) )) )[1]
			binaryParam_green = re.split( "[']", str(float_to_binary_string( float(temperature_green) )) )[1]
			binaryParam_blue = re.split( "[']", str(float_to_binary_string( float(temperature_blue) )) )[1]
			
			temperature = '00409c45'+binaryParam_red+binaryParam_green+binaryParam_blue

			#print 'temperature ', temperature



		if input_string.split(' ')[0]=='vibrance':
			vibrance_vibrance = input_string.split(' ')[2]
			
			binaryParam_vibrance = re.split( "[']", str(float_to_binary_string( float(vibrance_vibrance) )) )[1]
			

			vibrance = binaryParam_vibrance


		if input_string.split(' ')[0]=='colorcorrection':
			colorcorrection_highX = input_string.split(' ')[2]
			colorcorrection_highY = input_string.split(' ')[3]
			colorcorrection_shadX = input_string.split(' ')[4]
			colorcorrection_shadY = input_string.split(' ')[5]
			colorcorrection_saturation = input_string.split(' ')[6]
			
			binaryParam_highX = re.split( "[']", str(float_to_binary_string( float(colorcorrection_highX) )) )[1]
			binaryParam_highY = re.split( "[']", str(float_to_binary_string( float(colorcorrection_highY) )) )[1]
			binaryParam_shadX = re.split( "[']", str(float_to_binary_string( float(colorcorrection_shadX) )) )[1]
			binaryParam_shadY = re.split( "[']", str(float_to_binary_string( float(colorcorrection_shadY) )) )[1]
			binaryParam_ccSat = re.split( "[']", str(float_to_binary_string( float(colorcorrection_saturation) )) )[1]

			colorcorrection = binaryParam_highX+binaryParam_highY+binaryParam_shadX+binaryParam_shadY+binaryParam_ccSat


		if input_string.split(' ')[0]=='colorcontrast':
			colorcontrast_GM = input_string.split(' ')[2]
			colorcontrast_BY = input_string.split(' ')[3]
			
			binaryParam_GM = re.split( "[']", str(float_to_binary_string( float(colorcontrast_GM) )) )[1]
			binaryParam_BY = re.split( "[']", str(float_to_binary_string( float(colorcontrast_BY) )) )[1]

			colorcontrast = binaryParam_GM+'00000000'+binaryParam_BY+'0000000001000000'

	f.close()


	f = open(XMPdataFile_name, 'w')
	f.write('flip : ffffffff\n')
	f.write('exposure : '+exposure+'\n')
	f.write('shadhi : '+shadhi+'\n')
	f.write('colisa : '+colisa+'\n')
	f.write('temperature : '+temperature+'\n')
	f.write('vibrance : '+vibrance+'\n')
	f.write('colorcorrection : '+colorcorrection+'\n')
	f.write('colorcontrast : '+colorcontrast+'\n')
	f.close()

	#print 'finished'



