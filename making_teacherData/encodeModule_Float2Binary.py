import sys
import struct
import binascii


def float_to_binary_string(floatValue):
	binStr = binascii.b2a_hex( struct.pack("f", floatValue) )
	return binStr

def encode_f2b(paramfile_name, XMPdataFile_name):
	
	f = open(paramfile_name, 'r')
	for input_string in f:

		if input_string.split(' ')[0]=='exposure':
			exposure_black = input_string.split(' ')[2]
			exposure_exposure = input_string.split(' ')[3]

			binaryParam_black = float_to_binary_string( float(exposure_black) )
			binaryParam_exposure = float_to_binary_string( float(exposure_exposure) )

			exposure = '00000000'+binaryParam_black+binaryParam_exposure+'00004842000080c0'		

		if input_string.split(' ')[0]=='shadhi':
			shadhi_shadow = input_string.split(' ')[2]
			shadhi_whitepoint = input_string.split(' ')[3]
			shadhi_highlight = input_string.split(' ')[4]
			shadhi_shadowSat = input_string.split(' ')[5]
			shadhi_highlightSat = input_string.split(' ')[6]

			binaryParam_shadow = float_to_binary_string( float(shadhi_shadow) )
			binaryParam_whitepoint = float_to_binary_string( float(shadhi_whitepoint) )
			binaryParam_highlight = float_to_binary_string( float(shadhi_highlight) )
			binaryParam_shadowSat = float_to_binary_string( float(shadhi_shadowSat) )
			binaryParam_highlightSat = float_to_binary_string( float(shadhi_highlightSat) )
			
			shadhi = '000000000000c842'+binaryParam_shadow+binaryParam_whitepoint+binaryParam_highlight+'0000000000004842'+binaryParam_shadowSat+binaryParam_highlightSat+'7f000000bd37863500000000'
			
		if input_string.split(' ')[0]=='colisa':
			colisa_contrast = input_string.split(' ')[2]
			colisa_light = input_string.split(' ')[3]
			colisa_saturation = input_string.split(' ')[4]
			
			binaryParam_contrast = float_to_binary_string( float(colisa_contrast) )
			binaryParam_light = float_to_binary_string( float(colisa_light) )
			binaryParam_saturation = float_to_binary_string( float(colisa_saturation) )
			
			colisa = binaryParam_contrast+binaryParam_light+binaryParam_saturation

		if input_string.split(' ')[0]=='temperature':
			temperature_red = input_string.split(' ')[2]
			temperature_green = input_string.split(' ')[3]
			temperature_blue = input_string.split(' ')[4]
			
			binaryParam_red = float_to_binary_string( float(temperature_red) )
			binaryParam_green = float_to_binary_string( float(temperature_green) )
			binaryParam_blue = float_to_binary_string( float(temperature_blue) )
			
			temperature = '00409c45'+binaryParam_red+binaryParam_green+binaryParam_blue


		if input_string.split(' ')[0]=='vibrance':
			vibrance_vibrance = input_string.split(' ')[2]
			
			binaryParam_vibrance = float_to_binary_string( float(vibrance_vibrance) )

			vibrance = binaryParam_vibrance

		if input_string.split(' ')[0]=='colorcorrection':
			colorcorrection_highX = input_string.split(' ')[2]
			colorcorrection_highY = input_string.split(' ')[3]
			colorcorrection_shadX = input_string.split(' ')[4]
			colorcorrection_shadY = input_string.split(' ')[5]
			colorcorrection_saturation = input_string.split(' ')[6]
			
			binaryParam_highX = float_to_binary_string( float(colorcorrection_highX) )
			binaryParam_highY = float_to_binary_string( float(colorcorrection_highY) )
			binaryParam_shadX = float_to_binary_string( float(colorcorrection_shadX) )
			binaryParam_shadY = float_to_binary_string( float(colorcorrection_shadY) )
			binaryParam_ccSat = float_to_binary_string( float(colorcorrection_saturation) )

			colorcorrection = binaryParam_highX+binaryParam_highY+binaryParam_shadX+binaryParam_shadY+binaryParam_ccSat

		if input_string.split(' ')[0]=='colorcontrast':
			colorcontrast_GM = input_string.split(' ')[2]
			colorcontrast_BY = input_string.split(' ')[3]
			
			binaryParam_GM = float_to_binary_string( float(colorcontrast_GM) )
			binaryParam_BY = float_to_binary_string( float(colorcontrast_BY) )

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
