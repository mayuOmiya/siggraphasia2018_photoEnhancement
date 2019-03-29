import sys

#argvs = sys.argv
#inputImage = argvs[1]
#outputXMP = inputImage.split('.')[0]+'_new.xmp'


def makeXMP_file(inputImage, xmpFileData, outputXMP):
	#tempName = inputImage.split('/')
	#tempName2 = tempName[len(tempName)-1]

	
	#get parameter
	f = open(xmpFileData, 'r')
	for input_string in f:
		if input_string.split(' ')[0]=='exposure':
			newExposure = input_string.split(' ')[2].split('\n')[0]
		if input_string.split(' ')[0]=='shadhi':
			newShadhi = input_string.split(' ')[2].split('\n')[0]		
		if input_string.split(' ')[0]=='colisa':
			newColisa = input_string.split(' ')[2].split('\n')[0]
		if input_string.split(' ')[0]=='temperature':
			newTemperature = input_string.split(' ')[2].split('\n')[0]	
		if input_string.split(' ')[0]=='vibrance':
			newVibrance = input_string.split(' ')[2].split('\n')[0]	
		if input_string.split(' ')[0]=='colorcorrection':
			newColorCorrection = input_string.split(' ')[2].split('\n')[0]
		if input_string.split(' ')[0]=='colorcontrast':
			newColorContrast = input_string.split(' ')[2].split('\n')[0]	
	f.close()


	#road XMPtemplate
	f = open("mytemplate4.xmp", 'r')
	string = f.readlines()
	#print string
	f.close()

	for i in range(len(string)):
		if ('DerivedFrom' in string[i]):
			string[i] = '   xmpMM:DerivedFrom="'+inputImage+'"\n'
			#print string[i]

		if ('<darktable:history_params>' in string[i]):
			string[i+3] = '     <rdf:li>'+newExposure+'</rdf:li>\n'
			string[i+4] = '     <rdf:li>'+newShadhi+'</rdf:li>\n'
			string[i+5] = '     <rdf:li>'+newColisa+'</rdf:li>\n'
			string[i+6] = '     <rdf:li>'+newTemperature+'</rdf:li>\n'
			string[i+7] = '     <rdf:li>'+newVibrance+'</rdf:li>\n'
			string[i+8] = '     <rdf:li>'+newColorCorrection+'</rdf:li>\n'
			string[i+9] = '     <rdf:li>'+newColorContrast+'</rdf:li>\n'
			#print string[i]


	f = open(outputXMP, 'w')
	f.writelines(string)
	f.close()

