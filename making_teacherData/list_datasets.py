import glob
import sys

argvs = sys.argv
date = argvs[1]

dir_name = 'datasets/'

all_images = glob.glob( dir_name+'input_images/*' )
number = 0
with open( 'datasets/'+date+'_datasets''.txt', 'w' ) as file:
	for f in all_images:
		strings = (f.split('/')[-1])
		if ( strings.startswith(date) ):	
			file.write( strings+'\n')
			number += 1
