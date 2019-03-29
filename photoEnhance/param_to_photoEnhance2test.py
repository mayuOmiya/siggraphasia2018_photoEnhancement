import numpy as np
import sys

#import commands
import subprocess
import encodeModule_Float2Binary_p3 as encodeF2B
import makeXMLfileModule as makeXML

def make_parameter_file(parameter, paramfile_name): #ndarray params -> .txt memo

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
	
	f.write('exposure : '+exposure+'\n')
	f.write('shadhi : '+shadhi+'\n')
	f.write('colisa : '+colisa+'\n')
	f.write('temperature : '+temperature+'\n')
	f.write('vibrance : '+vibrance+'\n')
	f.write('colorcorrection : '+colorcorrection+'\n')
	f.write('colorcontrast : '+colorcontrast+'\n')
	f.close()

def param_to_photoEnhance(parameter, paramfile_name, input_dirName, output_dirName, mode):
	input_dirName = input_dirName + '/'
	output_dirName = output_dirName + '/'

	memoFileName = output_dirName+paramfile_name.split('.')[0]+'_parameter_cnn.txt'
	make_parameter_file(parameter, memoFileName) #ndarray params -> .txt memo

	XMPdataFile_name = output_dirName + paramfile_name.split('.')[0] + '_XMPdata_cnn.txt'
	encodeF2B.encode_f2b(memoFileName, XMPdataFile_name) #.txt memo -> binary

	#input_imX = input_dirName + mode + '/' + paramfile_name + '-s.png'
	input_imX = input_dirName  + paramfile_name

	xmpfile_name = output_dirName + paramfile_name.split('.')[0] + '_cnn.xmp'
	makeXML.makeXMP_file(input_imX, XMPdataFile_name, xmpfile_name) # binary -> xmp file

	#enhance photo
	output_im = output_dirName + paramfile_name.split('.')[0] + '_cnn.jpg'
	#enhancedImage = commands.getoutput('darktable-cli '+input_imX+' '+xmpfile_name+' '+output_im+' --hq false')
	enhancedImage = subprocess.call(['darktable-cli', input_imX, xmpfile_name, output_im, '--hq false'])


if __name__ == '__main__':

	input_dirName = '/home/omiya/data/flickr_teacherData0319/'
	argvs = sys.argv
	paramfile_name = argvs[1]

	descaled_params = np.array([  1.77958256e-03,  8.14358853e-04,  9.69827270e+00,  4.86786526e-04,  -4.35810558e+01,  6.95735470e+01,  5.39768246e+01,  6.27044122e-04,  -1.22064441e-05,  4.90333505e-01,  7.71161062e-01,  9.17773847e-01,  1.11711407e+00,  2.88826552e+01,  6.69432203e-04,  7.88821020e-04,  8.61634941e-04,  5.73705458e-04,  6.41476199e-01,  7.70902201e-01,  1.25244130e+00 ])
	mode = 'test'
	#paramfile_name = 'a1401'
	output_dirName = '/home/omiya/data/result0312/'
	print (descaled_params)

	param_to_photoEnhance(descaled_params, paramfile_name, output_dirName, mode)
