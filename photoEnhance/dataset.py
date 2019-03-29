import torch
import numpy as np
import pandas as pd
import os

from PIL import Image
from torch.utils.data import Dataset
from normalize import normalize

class FlickrInteresting(Dataset): #flickr dataset

	def __init__(self, csv_file, root, input_transform, mode='train'):

		self.root_dir = root
		self.csv_file = os.path.join(root, csv_file)
		self.enhance_param_frame = pd.read_csv(self.csv_file)
		self.mode = mode
		self.images = {}
		
		self.input_transform = input_transform

	def __getitem__(self, index):
		
		img_name = str(self.root_dir)+'/'+str(self.enhance_param_frame.ix[index, 0])

		image = self.images.get( img_name )
		if not image:
			with open(img_name, 'rb') as f:
				image = Image.open(f).convert('RGB')

			if( len(self.images)<50000 ): #to reduce memory usage
				self.images[img_name] = image 

		if self.mode == 'train' or self.mode == 'val':
			enhance_param = self.enhance_param_frame.ix[index, 1:].as_matrix().astype('float')

			enhance_param = normalize(enhance_param)
			enhance_param = torch.from_numpy(enhance_param).float() #ndarray -> tensor

		
		image = self.input_transform(image)

		if self.mode == 'test':
			enhance_param = []

		if self.mode == 'train':
			return image, enhance_param
		else: #val or test
			fileName0 = img_name.split('/')[-1]
			fileName = fileName0
			return image, enhance_param, fileName


	def __len__(self): #the size of the dataset
		return len(self.enhance_param_frame)

