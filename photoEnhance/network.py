import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models

class myVGG19_bn(nn.Module):

	def __init__(self, num_parameters):
		super(myVGG19_bn, self).__init__()

		vgg19_base = models.vgg19_bn(pretrained=True)
		
		self.features = vgg19_base.features
		self.classifier = vgg19_base.classifier
		self.classifier._modules['6'] = nn.Linear(4096, num_parameters)

	def forward(self, x):

		x = self.features(x)
		x = x.view(x.size(0), -1)
		y = self.classifier(x)

		return y

