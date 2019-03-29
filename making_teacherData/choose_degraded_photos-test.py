import torch
import os
import time
import sys
import datetime

from PIL import Image
from argparse import ArgumentParser

from torch.optim import SGD, Adam, Adadelta
from torch.autograd import Variable
from torchvision.transforms import Compose, Scale, CenterCrop, Normalize, RandomHorizontalFlip, RandomCrop
from torchvision.transforms import ToTensor, ToPILImage
from torch.utils.data import DataLoader
from collections import OrderedDict

from network import doubleVGG19_bn
from dataset import FlickrInterestingDouble

def test(test_loader, model, save_dir, date):
	model.eval()

	datedir = save_dir+date
	
	output_result = []
	file_names = []

	model = model.cuda()

	for step, (images, annotated_class, fileName) in enumerate(test_loader):
		
		images_bad = images[0].cuda()
		images_orig = images[1].cuda()
		inputs_bad = Variable(images_bad)
		inputs_orig = Variable(images_orig)
		
		outputs = model( (inputs_bad, inputs_orig) )
		output_float = float(outputs.data.cpu().numpy()[0])
		fileName = fileName[0]

		print( fileName, str(output_float) )
		output_result.append(output_float)
		file_names.append(fileName)


	resultFile = open(datedir+'/chosen_photos_'+str(date)+'.txt', 'w')
	for i in range(len(output_result)):
		resultFile.write(str(file_names[i])+' '+str(output_result[i])+'\n')
	resultFile.close()


def main(args):
	todaydetail = datetime.datetime.today()

	NUM_CLASSES = 1 #Y/N

	input_bad_mean = [ 0.37893708, 0.40996085, 0.39908306 ] #calculate from train dataset
	input_orig_mean = [  0.41886282,  0.39715287,  0.35399246 ]  
	input_std = [ 0.33, 0.33, 0.33 ] # (use "calc_MinStd.py")

	savedir = 'flickr-data/'


	image_transform = ToPILImage()
	input_bad_transform_train = Compose([
		Scale((256,256)),
		RandomCrop(224),
		RandomHorizontalFlip(),
		ToTensor(),
		Normalize(input_bad_mean, input_std)
	])
	input_orig_transform_train = Compose([
		Scale((256,256)),
		RandomCrop(224),
		RandomHorizontalFlip(),
		ToTensor(),
		Normalize(input_orig_mean, input_std)
	])

	input_bad_transform_testval = Compose([
		Scale((224,224)),
		ToTensor(),
		Normalize(input_bad_mean, input_std)
	])
	input_orig_transform_testval = Compose([
		Scale((224,224)),
		ToTensor(),
		Normalize(input_orig_mean, input_std)
	])
	
	if args.model == 'VGG19_bn':
		model = doubleVGG19_bn( NUM_CLASSES )
	else:
		print('check the model name')


	print(model)
	model.cuda()
	"""
	if args.multiGpu == 1:
		model = torch.nn.DataParallel(model)
	"""
	model = torch.nn.DataParallel(model)

	weight = torch.ones(NUM_CLASSES)
	criterion = torch.nn.BCEWithLogitsLoss().cuda()
	
	if args.mode == 'test':
		print('test...')

		#savedData = 'ite_'+str(args.iteration)+'_net.pth'
		savedData = 'classification_net.pth'
				
		state = torch.load(savedData)
		"""
		# create new OrderedDict that does not contain `module.`
		new_state = OrderedDict()
		for k, v in state.items():
			name = k[7:] # remove `module.`
			new_state[name] = v
		# load params
		model.load_state_dict(new_state)
		"""
		if 'state_dict' in state and 'iteration' in state:
			model.load_state_dict(state['state_dict'])
			iteration = state['iteration']
			#downSize = state['downSize']
		else:
			model.load_state_dict(state)
			#iteration = args.iteration
			iteration = '47500'
		
		datedir = args.datedir
		test_dataset = FlickrInterestingDouble('all_bad_file_name.txt', savedir, datedir, input_bad_transform_testval, input_orig_transform_testval, mode='test')
		test_loader = DataLoader(test_dataset, num_workers=args.num_workers, batch_size=1, shuffle=False, drop_last=False)
		test(test_loader, model, savedir, datedir)
		
if __name__ == '__main__':
	parser = ArgumentParser()

	subparsers = parser.add_subparsers(dest='mode')
	subparsers.required = True

	parser_test = subparsers.add_parser('test')
	#parser_test.add_argument('--savedir', type=str, required=True)
	#parser_test.add_argument('--directry-date', default='201805271839')
	#parser_test.add_argument('--iteration', type=int, default=47500)
	parser_test.add_argument('--model', type=str, default='VGG19_bn')
	parser_test.add_argument('--num-workers', type=int, default=0)
	parser_test.add_argument('--multiGpu', type=int, default=0)
	parser_test.add_argument('--datedir', type=str, required=True) #2019-01-31


	main(parser.parse_args())


