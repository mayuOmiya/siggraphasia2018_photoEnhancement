import torch
import numpy as np
import os

from PIL import Image
from torch.utils.data import Dataset

def load_image(file):
	return Image.open(file)


class FlickrInterestingDouble(Dataset): #flickr dataset original image & bad image

	def __init__(self, txt_file, root, datedir, input_bad_transform, input_orig_transform, mode='train'):

		self.root_dir = root
		self.datedir = datedir
		self.txt_file = os.path.join(root, datedir, txt_file)
		#self.enhance_param_frame = pd.read_csv(self.csv_file)
		with open(self.txt_file, 'r') as file:
			self.image_files = file.readlines()

		self.mode = mode
		
		self.input_bad_transform = input_bad_transform
		self.input_orig_transform = input_orig_transform

	def __getitem__(self, index):

		temp_img = str(self.image_files[index]).split('\n')[0]
		bad_img_name = str(self.root_dir)+'degraded_photos/temp/'+temp_img #bad img
		orig_img_name = str(self.root_dir)+str(self.datedir)+'/'+temp_img.split("_bad.jpg")[0]+'.jpg'  #original img

		with open(bad_img_name, 'rb') as f:
			bad_image = load_image(f).convert('RGB')
		with open(orig_img_name, 'rb') as f:
			orig_image = load_image(f).convert('RGB')

		bad_image = self.input_bad_transform(bad_image)
		orig_image = self.input_orig_transform(orig_image)
		
		if self.mode == 'test':
			annotated_class = []

		images = [ bad_image, orig_image ]

		fileName = bad_img_name.split('/')[-1]
		return images, annotated_class, fileName


	def __len__(self): #the size of the dataset
		return len(self.image_files)

