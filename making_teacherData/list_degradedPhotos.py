import glob
import sys

argvs = sys.argv
date = argvs[1]
#date = '2019-01-31'

all_bad_images = glob.glob( 'flickr-data/degraded_photos/temp/*' )

with open( 'flickr-data/'+date+'/all_bad_file_name.txt', 'w' ) as file:
	for f in all_bad_images:
		strings = (f.split('/')[-1])
		if ( strings.startswith(date) ):
			if ( not f.endswith('parameter_bad.txt') ):
				file.write( strings+'\n')