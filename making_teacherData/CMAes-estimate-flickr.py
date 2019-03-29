import cma
import numpy as np
import sys
import os.path
import subprocess
from PIL import Image

import encodeModule_Float2Binary_py3 as encodeF2B
import makeXMLfileModule_py3 as makeXML

#change here
#source_directry_name = '/home/omiya/data/Flickr_Interestingness1109/'
#bad_image_dir = '/home/omiya/data/Flickr_Interestingness1109/degraded_photos/chosen/'
#estimated_dir = '/home/omiya/data/Flickr_Interestingness1109/estimated_images/'

source_directry_name = 'flickr-data/'
bad_image_dir = 'flickr-data/degraded_photos/chosen/'
estimated_dir = 'flickr-data/estimated_images/'

def make_parameter_file(parameter):

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
	#f = open('tempParameter.txt', 'w')
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

	
def objectFunc(parameter): # x=original image, z=target image
	
	make_parameter_file(parameter)
	encodeF2B.encode_f2b(paramfile_name, XMPdataFile_name)
	makeXML.makeXMP_file(input_imX, XMPdataFile_name, xmpfile_name)
	
	if os.path.exists( output_imY ):
		subprocess.call( ['mv', output_imY, output_prev] )

	devnull = open('/dev/null', 'w')
	subprocess.call( ['darktable-cli', input_imX, xmpfile_name, output_imY, '--hq false' ], stdout=devnull, stderr=devnull )
	
	return np.array( Image.open( output_imY ) ).astype(np.float64)/255.0


if __name__ == '__main__':
	
	argvs = sys.argv
	input_name = argvs[1] #2019-01-31-***

	#input file
	#input_imZ = source_directry_name + 'original_photos/' + input_name[:10] + '/' + input_name + '.jpg'

	input_imZ = source_directry_name + input_name[:10] + '/' + input_name + '.jpg'
	input_imX = bad_image_dir + input_name +'_bad.jpg'
	original_param = bad_image_dir + input_name +'_parameter_bad.txt'

	#output file
	paramfile_name = estimated_dir + 'parameters/' + input_name +'_parameter_cma.txt'
	XMPdataFile_name = estimated_dir + 'xmpFiles/' + input_name +'_tempXMPdata_cma.txt'
	xmpfile_name = estimated_dir + 'xmpFiles/' + input_name +'_cma.xmp'
	output_imY = estimated_dir + 'reproducedImages/' + input_name + '_new_cma.jpg'
	output_prev = estimated_dir + 'reproducedImages/' + input_name +'_prev_cma.jpg'


	if not os.path.exists(estimated_dir + 'parameters/'):
		os.mkdir(estimated_dir + 'parameters/')
	if not os.path.exists(estimated_dir + 'xmpFiles/'):
		os.mkdir(estimated_dir + 'xmpFiles/')
	if not os.path.exists(estimated_dir + 'reproducedImages/'):
		os.mkdir(estimated_dir + 'reproducedImages/')
			
	opts = cma.CMAOptions()
	opts['seed'] = 1234
	opts['CMA_stds'] = [ 0.1, 0.75, 100, 10, 87.5, 50, 50, 0.5, 0.625, 0.625, 0.5, 0.5, 0.5, 50, 40, 40, 40, 40, 0.5, 0.2, 0.2 ]
	opts['ftarget'] = 1.0e-5
	opts['tolfun'] = 1.0e-3
	opts['popsize'] = 10
	opts['maxiter'] = 300
	opts['verb_filenameprefix'] = estimated_dir+'log/'+input_name


	if os.path.isfile(input_imX) and os.path.isfile(input_imZ):

		print( input_imX )
		print( input_imZ )

		#initial_param = read_param( original_param )  #use degraded params
		initial_param = np.array( [0, 0, 50, 0, -50, 100, 50, 0, 0, 0.5, 1, 1, 1, 25, 0, 0, 0, 0, 1, 1, 1] ) 
		print( initial_param )

		#get image
		x = np.array( Image.open( input_imX ) ).astype(np.float64)/255.0
		z = np.array( Image.open( input_imZ ) ).astype(np.float64)/255.0

		loss = lambda param: np.mean( np.power( z-objectFunc(param), 2 ) )
		optimized_param = cma.fmin(loss, initial_param, 0.5, opts)
		
		#make new image
		print( '\nbest evaluated solution:', optimized_param[0] )
		print( '\niterations:', optimized_param[4] )
		print( 'respective function value:', optimized_param[1] )

		objectFunc(optimized_param[0])

		subprocess.call( ['rm', output_prev] )

	elif os.path.isfile(input_imZ):
		print( input_imX, 'is not exist.' )
	else:
		print( input_imZ, 'is not exist.' )

