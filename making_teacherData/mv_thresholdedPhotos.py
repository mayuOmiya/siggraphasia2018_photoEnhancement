import shutil
import sys
import subprocess
import os

date = sys.argv[1] #'2019-01-31'

file_name = 'flickr-data/'+date+'/chosen_photos_'+date+'_2.5.txt'
src_dir = 'flickr-data/degraded_photos/temp/'
dst_chosen = 'flickr-data/degraded_photos/chosen/'
dst_notChosen = 'flickr-data/degraded_photos/not_chosen/'

if not os.path.exists(dst_chosen):
	os.mkdir(dst_chosen)
if not os.path.exists(dst_notChosen):
	os.mkdir(dst_notChosen)

with open( file_name, 'r' )as file:
	all_photos = file.readlines()

photos_num = len(all_photos)
results = [ 0 ]*photos_num
photos_name = [ '' ]*photos_num
params_name = ['']*photos_num
chosen_num = 0
not_chosen_num = 0

for i in range(photos_num):
	results[i] =  int(str(all_photos[i])[-2:-1])
	photos_name[i] = str(all_photos[i]).split(' ')[0]
	params_name[i] = str(all_photos[i]).split('_bad')[0]+'_parameter_bad.txt'
	if (results[i]): #chosen
		chosen_num += 1
		if os.path.exists(src_dir+photos_name[i]):
			#print(photos_name[i])
			shutil.move( src_dir+photos_name[i], dst_chosen+photos_name[i] )
		if os.path.exists(src_dir+params_name[i]):
                        #print(photos_name[i])
                        shutil.move( src_dir+params_name[i], dst_chosen+params_name[i] )

	else: #not chosen
		not_chosen_num += 1
		if os.path.exists(src_dir+photos_name[i]):
			shutil.move( src_dir+photos_name[i], dst_notChosen+photos_name[i] )
		if os.path.exists(src_dir+params_name[i]):
                        shutil.move( src_dir+params_name[i], dst_notChosen+params_name[i] )

print(chosen_num, not_chosen_num)
