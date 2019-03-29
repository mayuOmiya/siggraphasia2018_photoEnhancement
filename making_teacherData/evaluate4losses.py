import numpy as np
import sys
import os.path

from PIL import Image
from skimage import color
from skimage.measure import compare_ssim as ssim

#evaluate 4 losses: Lab, H, S, SSIM

#get image
argvs = sys.argv
input_name = argvs[1]

date = input_name[0:10]

#change here
"""
bad_image_dir = '/home/omiya/data/Flickr_Interestingness1109/degraded_photos/chosen/'
source_image_dir = '/home/omiya/data/Flickr_Interestingness1109/original_photos/'+date+'/'
estimated_image_dir = '/home/omiya/data/Flickr_Interestingness1109/estimated_images/reproducedImages/'
evaluate_dir = '/home/omiya/data/Flickr_Interestingness1109/estimated_images/evaluate/'
"""
bad_image_dir = 'flickr-data/degraded_photos/chosen/'
source_image_dir = 'flickr-data/'+date+'/'
estimated_image_dir = 'flickr-data/estimated_images/reproducedImages/'
evaluate_dir = 'flickr-data/estimated_images/evaluate/'

img_input = bad_image_dir + input_name + '_bad.jpg'
img_original = source_image_dir + input_name + '.jpg'


optimizationMethod = 'cma'
img_reproduced = estimated_image_dir + input_name +  '_new_' + optimizationMethod + '.jpg'

if (os.path.exists(img_input) and os.path.exists(img_reproduced)):

	print(img_input) #bad
	print(img_original) #original
	print(img_reproduced) #reproduced
	output_name = evaluate_dir + 'result_' + input_name +  '_' + optimizationMethod + '.txt'

	#RGB
	img_input_rgb = np.array( Image.open( img_input ) ).astype(np.float64)/255.0
	img_original_rgb = np.array( Image.open( img_original ) ).astype(np.float64)/255.0
	img_reproduced_rgb = np.array( Image.open( img_reproduced ) ).astype(np.float64)/255.0

	loss_io_rgb = np.mean( np.power( img_input_rgb-img_original_rgb, 2 ) )
	loss_ro_rgb = np.mean( np.power( img_reproduced_rgb-img_original_rgb, 2 ) )

	print('RGB')
	print( 'Loss (De-enhanced image - Original) : ', loss_io_rgb )
	print( 'Loss (Reproduced image - Original)  : ', loss_ro_rgb, '\n' )

	#Lab
	img_input_lab = color.rgb2lab( img_input_rgb )
	img_original_lab = color.rgb2lab( img_original_rgb )
	img_reproduced_lab = color.rgb2lab( img_reproduced_rgb )

	loss_io_lab = np.mean( np.power( img_input_lab-img_original_lab, 2 ) )
	loss_ro_lab = np.mean( np.power( img_reproduced_lab-img_original_lab, 2 ) )
	
	print('Lab')
	print( 'Loss (De-enhanced image - Original) : ', loss_io_lab )
	print( 'Loss (Reproduced image - Original)  : ', loss_ro_lab, '\n' )

	#HSV
	img_input_hsv = color.rgb2hsv( img_input_rgb )
	img_original_hsv = color.rgb2hsv( img_original_rgb )
	img_reproduced_hsv = color.rgb2hsv( img_reproduced_rgb )

	loss_io_hsv_s = np.mean( np.power( img_input_hsv[:,:,1]-img_original_hsv[:,:,1], 2 ) )
	loss_ro_hsv_s = np.mean( np.power( img_reproduced_hsv[:,:,1]-img_original_hsv[:,:,1], 2 ) )
	
	print('HSV')
	print( 'Loss (De-enhanced image - Original) : ', loss_io_hsv_s )
	print( 'Loss (Reproduced image - Original)  : ', loss_ro_hsv_s, '\n' )

	#SSIM
	loss_io_SSIM = ssim(img_input_hsv[:,:,2], img_original_hsv[:,:,2]) #grayscale = v
	loss_ro_SSIM = ssim(img_reproduced_hsv[:,:,2], img_original_hsv[:,:,2]) #grayscale = v

	print('SSIM')
	print( 'Loss (De-enhanced image - Original) : ', 1-loss_io_SSIM )
	print( 'Loss (Reproduced image - Original)  : ', 1-loss_ro_SSIM, '\n' )
	
	print('Loss (Reproduced image - Original)  : RGB, Lab, S, 1-SSIM' )
	print(loss_ro_rgb, loss_ro_lab, loss_ro_hsv_s, 1-loss_ro_SSIM)

	with open(output_name, mode='w') as f:
		f.write('RGB')
		f.write( 'Loss (De-enhanced image - Original) : '+str(loss_io_rgb) )
		f.write( 'Loss (Reproduced image - Original)  : '+str(loss_ro_rgb)+'\n' )
		f.write('Lab')
		f.write( 'Loss (De-enhanced image - Original) : '+str(loss_io_lab) )
		f.write( 'Loss (Reproduced image - Original)  : '+str(loss_ro_lab)+'\n' )
		f.write('HSV_s')
		f.write( 'Loss (De-enhanced image - Original) : '+str(loss_io_hsv_s) )
		f.write( 'Loss (Reproduced image - Original)  : '+str(loss_ro_hsv_s)+'\n' )
		f.write('SSIM')
		f.write( 'Loss (De-enhanced image - Original) : '+str(1-loss_io_SSIM) )
		f.write( 'Loss (Reproduced image - Original)  : '+str(1-loss_ro_SSIM)+'\n\n' )

		f.write('Loss (Reproduced image - Original)  : RGB Lab S 1-SSIM\n' )
		f.write(str(loss_ro_rgb)+' '+str(loss_ro_lab)+' '+str(loss_ro_hsv_s)+' '+str(1-loss_ro_SSIM))


elif (os.path.exists(img_input)):
	print(img_reproduced , 'is not exists.')
else:
	print(img_input , 'is not exists.')



