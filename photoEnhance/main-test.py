import torch
import os
import time
import sys
import datetime

from PIL import Image
from argparse import ArgumentParser
from collections import OrderedDict

from torch.optim import SGD, Adam, Adadelta
from torch.autograd import Variable
from torchvision.transforms import Compose, Scale, CenterCrop, Normalize, RandomHorizontalFlip, RandomCrop
from torchvision.transforms import ToTensor, ToPILImage
from torch.utils.data import DataLoader

from network import myVGG19_bn
from dataset import FlickrInteresting
from normalize import denormalize
import param_to_photoEnhance2test

def test(test_loader, model, data_dir, save_dir, iteration):
	model.eval()

	itedir_out = os.path.join(save_dir, 'testResults', str(iteration))
	if not os.path.exists( os.path.join(save_dir, 'testResults') ):
		os.mkdir( os.path.join(save_dir, 'testResults') )
	if not os.path.exists(itedir_out):
		os.mkdir(itedir_out)

	
	model = model.cuda()

	print('def test')
	

	for step, (images, enhance_params, fileName) in enumerate(test_loader):
		
		images = images.cuda()
		
		inputs = Variable(images, volatile=True)
		outputs = model(inputs)
		
		normalized_params = (outputs.data).cpu().numpy()
		denormalized_params = denormalize( normalized_params )
		#save descaled params, enhanced photos
		
		param_to_photoEnhance2test.param_to_photoEnhance( denormalized_params.flatten(), fileName[0], data_dir, itedir_out, 'test' )

		#scaled params -> descaled params, save
		#descaled params -> xmp file
		#enhanced_image, save


def main(args):
	todaydetail = datetime.datetime.today()

	NUM_PARAMETERS = 21

	input_mean = [ 0.43626672, 0.41767832, 0.36745313 ]
	input_std = [ 0.26666969999999998, 0.2542865, 0.2622691 ] 

	datadir = 'images/'
	traindir = os.path.join(datadir, 'train')
	valdir = os.path.join(datadir, 'val')
	testdir = os.path.join(datadir, 'test')

	image_transform = ToPILImage()
	input_transform_testval = Compose([
		Scale((224,224)),
		ToTensor(),
		Normalize(input_mean, input_std)
	])

	model = myVGG19_bn( NUM_PARAMETERS )
	#print(model)
	model.cuda()

	if args.multiGpu == 1:
		model = torch.nn.DataParallel(model)
	
	weight = torch.ones(NUM_PARAMETERS)
	criterion = torch.nn.MSELoss().cuda()
	


	if args.mode == 'test':
		
		dst = 'result'
		print(dst)
		if not os.path.exists(dst):
			os.mkdir(dst)
		savedData = 'photoEnhanceNet.pth'
		
		if not os.path.exists(dst+'/testResults'):
			os.mkdir(dst+'/testResults')
		
		state = torch.load(savedData)
		if 'state_dict' in state and 'iteration' in state:
			model.load_state_dict(state['state_dict'])
			iteration = state['iteration']
		else:
			model.load_state_dict(state)
			iteration = 6144

		test_dataset = FlickrInteresting('test-data.csv', testdir, input_transform_testval, 'test')
		test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False, drop_last=False)
		test(test_loader, model, testdir, dst, iteration)
		

if __name__ == '__main__':
	parser = ArgumentParser()
	

	subparsers = parser.add_subparsers(dest='mode')
	subparsers.required = True

	parser_test = subparsers.add_parser('test')
	#parser_test.add_argument('--datadir', type=str, required=True)
	#parser_test.add_argument('--savedir', type=str, required=True)
	#parser_test.add_argument('--directry-date', required=True)
	#parser_test.add_argument('--iteration', type=int, required=True)
	#parser_test.add_argument('--model', type=str, required=True)
	#parser_test.add_argument('--multiGpu', type=int, required=True) 
	parser_test.add_argument('--multiGpu', type=int, default=1) 

	main(parser.parse_args())


