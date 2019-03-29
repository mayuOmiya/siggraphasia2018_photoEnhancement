import sys
import os.path
import subprocess
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor


def thresholding(four_losses):

	#RGB, Lab, S, 1-SSIM
	X = [ [0.0019179818, 18.5595675216, 0.0123039612, 0.0360166465],
	[0.0004951584, 5.8433188704, 0.0047921501, 0.0149470892],
	[0.0014540104, 19.1402262621, 0.0252352933, 0.0336825143],
	[0.0025210192, 36.4735531281, 0.0105721705, 0.064282369],
	[0.0014862891, 23.5593892963, 0.022288504, 0.027101186],
	[0.0004871349, 12.4431798057, 0.0058280227, 0.0248436844],
	[0.0009471917, 10.1547320509, 0.0075287356, 0.0462014023],
	[0.0005253901, 4.4151976606, 0.0349305089, 0.0339421891],
	[0.0004698956, 10.3273312309, 0.0118247253, 0.0227674967],
	[0.0020320435, 23.849317618, 0.019317513, 0.06405533],
	[0.0016540007, 26.2328759267, 0.0213475485, 0.019925247],
	[0.0013103601, 21.0636998086, 0.0216519394, 0.0248256473],
	[0.000979428, 10.4972021806, 0.0096676359, 0.0103150603],
	[0.0016138709, 9.6098916522, 0.010885826, 0.0591854274],
	[0.003044981, 27.5288127465, 0.0097767535, 0.0528874775],
	[0.002228191, 11.9748724081, 0.0043473662, 0.0457419932],
	[0.0054892848, 60.3671027942, 0.0118557319, 0.1285617998],
	[0.0048412194, 26.6711021687, 0.0135154874, 0.0793831252],
	[0.0429926578, 261.4293438496, 0.0418320317, 0.1414524448],
	[0.0054328384, 37.8782069346, 0.0226921695, 0.0883558378],
	[0.0006333939, 12.0366540756, 0.0011068166, 0.0132659508],
	[0.003195794, 22.1537329962, 0.0092573839, 0.0878064843],
	[0.0072101384, 45.9244700239, 0.0175240134, 0.2022031495],
	[0.0059689538, 78.7906921379, 0.0263814657, 0.1114273394],
	[0.0021618044, 28.6433119448, 0.0092233771, 0.069292412],
	[0.0012929118, 13.7987750263, 0.0284239176, 0.0642519267],
	[0.0032468937, 40.5325627932, 0.0101015085, 0.0629441991],
	[0.003171312, 43.9432345649, 0.037428831, 0.0958434568],
	[0.0007238712, 12.291692841, 0.0064387022, 0.0109431453],
	[0.0016649992, 35.8811627621, 0.0144759563, 0.0239960587] ]

	Y = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	estimator = RandomForestRegressor(n_estimators=100, random_state=42)
	estimator.fit(X, Y)
	Y_pred = estimator.predict(four_losses)
	return Y_pred

if __name__ == '__main__':


	#get image
	argvs = sys.argv
	input_name = argvs[1]
	date = input_name[0:10]

	#change here
	"""
	bad_image_dir = '/home/omiya/data/Flickr_Interestingness1109/degraded_photos/chosen/'
	bad_param_dir = '/home/omiya/data/Flickr_Interestingness1109/degraded_parameters/'
	source_image_dir = '/home/omiya/data/Flickr_Interestingness1109/original_photos/'+date+'/'
	estimated_dir = '/home/omiya/data/Flickr_Interestingness1109/estimated_images/'
	estimated_image_dir = '/home/omiya/data/Flickr_Interestingness1109/estimated_images/reproducedImages/'
	evaluate_dir = '/home/omiya/data/Flickr_Interestingness1109/estimated_images/evaluate/'

	bad_image_dst_dir = '/home/omiya/data/Flickr_Datasets1109/input_images/'
	bad_param_dst_dir = '/home/omiya/data/Flickr_Datasets1109/degrade_parameters/'
	original_image_dst_dir = '/home/omiya/data/Flickr_Datasets1109/original_images/' 
	target_param_dst_dir = '/home/omiya/data/Flickr_Datasets1109/target/estimated_parameters/'
	estimated_dst_image_dir = '/home/omiya/data/Flickr_Datasets1109/target/estimated_images/'
	"""
	bad_image_dir = 'flickr-data/degraded_photos/chosen/'
	bad_param_dir = 'flickr-data/degraded_parameters/'
	source_image_dir = 'flickr-data/'+date+'/'
	estimated_dir = 'flickr-data/estimated_images/'
	estimated_image_dir = 'flickr-data/estimated_images/reproducedImages/'
	evaluate_dir = 'flickr-data/estimated_images/evaluate/'

	bad_image_dst_dir = 'datasets/input_images/'
	bad_param_dst_dir = 'datasets/degrade_parameters/'
	original_image_dst_dir = 'datasets/original_images/' 
	target_param_dst_dir = 'datasets/target/estimated_parameters/'
	estimated_dst_image_dir = 'datasets/target/estimated_images/'

	log_file = evaluate_dir+'result_'+input_name+'_cma.txt'
	thr = 0.5

	if os.path.exists(log_file):
		with open(log_file, 'r') as f:
			l_strip = [s.strip() for s in f.readlines()]
		losses = l_strip[-1]
		loss_rgb = losses.split(' ')[0]
		loss_lab = losses.split(' ')[1]
		loss_hsv_s = losses.split(' ')[2]
		loss_ssim = losses.split(' ')[3]
		four_losses = [ [ loss_rgb, loss_lab, loss_hsv_s, loss_ssim ] ]
		#print(four_losses)

		score = thresholding(four_losses)
		print(score)

		if(score>=thr): #estimate was succeded!
			print('ok')

			#bad image
			if os.path.exists(bad_image_dir+input_name+'_bad.jpg'):
				subprocess.call( ['cp', bad_image_dir+input_name+'_bad.jpg', bad_image_dst_dir+input_name+'_bad.jpg'] )
			else:
				print(bad_image_dir+input_name+'_bad.jpg is not exists.')
			#bad param
			if os.path.exists(bad_param_dir+input_name+'_parameter_bad.txt'):
				subprocess.call( ['cp', bad_param_dir+input_name+'_parameter_bad.txt', bad_param_dst_dir+input_name+'_parameter_bad.txt'] )
			else:
				print(bad_image_dir+input_name+'_parameter_bad.txt is not exists.')
			#original image
			if os.path.exists(source_image_dir+input_name+'.jpg'):
				subprocess.call( ['cp', source_image_dir+input_name+'.jpg', original_image_dst_dir+input_name+'.jpg'] )
			else:
				print(source_image_dir+input_name+'.jpg is not exists.')
			#target param, xmpFile, 
			if os.path.exists(estimated_dir+'parameters/'+input_name+'_parameter_cma.txt'):
				subprocess.call( ['cp', estimated_dir+'parameters/'+input_name+'_parameter_cma.txt', target_param_dst_dir+input_name+'_parameter_cma.txt'] )
				subprocess.call( ['cp', estimated_dir+'xmpFiles/'+input_name+'_cma.xmp', target_param_dst_dir+input_name+'_cma.xmp'] )
			else:
				print(estimated_dir+'parameters/'+input_name+'_parameter_cma.txt is not exists.')
			#target image(estimated_image)
			if os.path.exists(estimated_image_dir+input_name+'_new_cma.jpg'):
				subprocess.call( ['cp', estimated_image_dir+input_name+'_new_cma.jpg', estimated_dst_image_dir+input_name+'_new_cma.jpg'] )
			else:
				print(estimated_image_dir+input_name+'_new_cma.jpg is not exists.')

		else:#estimate was not succeded!
			print('thresholded')
	else:
		print(log_file, 'is not exists.')