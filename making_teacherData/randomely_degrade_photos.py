import os
import sys
import random
import numpy as np
import re
import commands
import encodeModule_Float2Binary as encodeF2B
import makeXMLfileModule as makeXML
from PIL import Image

argvs = sys.argv
date = argvs[1]
#date = '2019-01-31'

original_image_dir = 'flickr-data/'+date+'/'
bad_image_dir = 'flickr-data/degraded_photos/temp/'

if os.path.exists( 'flickr-data/degraded_photos/' ):
	if not os.path.exists( bad_image_dir ):
		os.mkdir( bad_image_dir )
else:
	os.mkdir( 'flickr-data/degraded_photos/' )
	os.mkdir( bad_image_dir )

f = open('flickr-data/'+date+'/all_file_name.txt', 'r')
file_name = f.readlines()
f.close()

def make_random_parameters():
	param_initial = [ 0, 0, 50, 0, -50, 100, 50, 0, 0, 0, 1, 1, 1, 25, 0, 0, 0, 0, 1, 1, 1 ]
	param_max = [ 0.1, 2.5, 100, 10, 100, 100, 100, 1.0, 1.0, 0.75, 1.2, 1.2, 1.2, 100, 20, 20, 20, 20, 1.5, 1.2, 1.2 ]
	param_min = [ -0.1, -2.5, -100, -10, -100, 0, 0, -1.0, -1.0, -1.0, 0.8, 0.8, 0.8, 0, -20, -20, -20, -20, 0.25, 0.8, 0.8 ]

	param_num = len(param_initial)
	random_param= [0]*param_num

	for i in range(param_num):
		random_param[i] = random.uniform(param_min[i], param_max[i])
	return random_param

def make_parameter_file(parameter, paramfile_name ):

	parameter[0] = np.clip(parameter[0], -0.1, 0.1) #exposre black
	parameter[1] = np.clip(parameter[1], -3, 3) 	#exposre exposure
	parameter[2] = np.clip(parameter[2], -100, 100) #shadhi shadow
	parameter[3] = np.clip(parameter[3], -10, 10)	#shadhi whitepoint
	parameter[4] = np.clip(parameter[4], -100, 100) #shadhi highlight
	parameter[5] = np.clip(parameter[5], 0, 100)	#shadhi shadowsaturation
	parameter[6] = np.clip(parameter[6], 0, 100)	#shadhi highlightsaturation
	parameter[7] = np.clip(parameter[7], -1, 1)		#colisa contrast
	parameter[8] = np.clip(parameter[8], -1, 1)		#colisa lightness
	parameter[9] = np.clip(parameter[9], -1, 1)		#colisa saturation
	parameter[10] = np.clip(parameter[10], 0, 8)	#temperature R
	parameter[11] = np.clip(parameter[11], 0, 8)	#temperature G
	parameter[12] = np.clip(parameter[12], 0, 8)	#temperature B
	parameter[13] = np.clip(parameter[13], 0, 100)	#vibrance vibrance
	parameter[14] = np.clip(parameter[14], -40, 40)	#colorcorrection highlightX
	parameter[15] = np.clip(parameter[15], -40, 40)	#colorcorrection highlightY
	parameter[16] = np.clip(parameter[16], -40, 40)	#colorcorrection shadowX
	parameter[17] = np.clip(parameter[17], -40, 40)	#colorcorrection shadowY
	parameter[18] = np.clip(parameter[18], -3, 3)	#colorcorrection saturation
	parameter[19] = np.clip(parameter[19], 0, 5)	#colorcontrast GM
	parameter[20] = np.clip(parameter[20], 0, 5)	#colorcontrast BY


	exposure = str(parameter[0])+' '+str(parameter[1])
	shadhi = str(parameter[2])+' '+str(parameter[3])+' '+str(parameter[4])+' '+str(parameter[5])+' '+str(parameter[6])
	colisa = str(parameter[7])+' '+str(parameter[8])+' '+str(parameter[9])
	temperature = str(parameter[10])+' '+str(parameter[11])+' '+str(parameter[12])
	vibrance = str(parameter[13])
	colorcorrection = str(parameter[14])+' '+str(parameter[15])+' '+str(parameter[16])+' '+str(parameter[17])+' '+str(parameter[18])
	colorcontrast = str(parameter[19])+' '+str(parameter[20])

	f = open(paramfile_name, 'w')
	#f.write('flip : ffffffff\n')
	f.write('exposure : '+exposure+'\n')
	f.write('shadhi : '+shadhi+'\n')
	f.write('colisa : '+colisa+'\n')
	f.write('temperature : '+temperature+'\n')
	f.write('vibrance : '+vibrance+'\n')
	f.write('colorcorrection : '+colorcorrection+'\n')
	f.write('colorcontrast : '+colorcontrast+'\n')
	f.close()

def make_retouched_photo(parameter, imgname ): # x=original image, z=target image

	input_name = re.split('[/.]', imgname)[-2] #2019-01-31-...
	paramfile_name = bad_image_dir + input_name + '_parameter_bad.txt'
	XMPdataFile_name = bad_image_dir + input_name + '_tempXMPdata_bad.txt'
	xmpfile_name = bad_image_dir + input_name + '_bad.xmp'
	output_im = bad_image_dir + input_name +'_bad.jpg'

	make_parameter_file( parameter, paramfile_name )
	#print 'made parameter file'
	encodeF2B.encode_f2b(paramfile_name, XMPdataFile_name)
	#print 'encoded'
	makeXML.makeXMP_file(imgname, XMPdataFile_name, xmpfile_name)
	#print 'made xmpFile'
	tempImage = commands.getoutput('darktable-cli '+imgname+' '+xmpfile_name+' '+output_im+' --hq false')
	commands.getoutput('rm '+XMPdataFile_name)
	commands.getoutput('rm '+xmpfile_name)


def make_bad_photo( imgname ):
	parameter = np.array( make_random_parameters() )
	make_retouched_photo( parameter, imgname )

def process_image( imgname ):
	#if not redo and imgname in annotations.keys():
	#	return True

	make_bad_photo( imgname )
	input_name = re.split('[/.]', imgname)[-2] #2019-01-31-...
	paramfile_name = bad_image_dir + input_name + '_parameter_bad.txt'
	bad_imgname = bad_image_dir + input_name +'_bad.jpg'
	org_imgname = imgname

	# Load and view the image
	if os.path.exists( bad_imgname ) and os.path.exists( org_imgname ):
		bad_img = Image.open( bad_imgname )
		org_img = Image.open( org_imgname )
	elif os.path.exists( org_imgname ):
		print(bad_imgname.split('/')[-1]+" can't be loaded")
	

for imgname in file_name:

	temp = imgname.split('\n')[0] #2019-01-31-...

	original_image_name = original_image_dir + temp + '.jpg'
	process_image( original_image_name )
	
