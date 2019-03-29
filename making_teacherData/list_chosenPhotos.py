import glob
import sys
import shutil

argvs = sys.argv
date = argvs[1] #'2019-01-31'
print(date)

all_chosen_images = glob.glob( 'flickr-data/degraded_photos/chosen/*' )

with open( 'flickr-data/'+date+'/all_chosen_degraded_file_name.txt', 'w' ) as file:
	for f in all_chosen_images:
		strings = (f.split('/')[-1]).split('_bad')[0]
		if ( strings.startswith(date) ):
			if ( not f.endswith('parameter_bad.txt') ):
				file.write( strings+'\n' )

shutil.copy2( 'flickr-data/'+date+'/all_chosen_degraded_file_name.txt', 'flickr-data/'+date+'/temp_file_name.txt')