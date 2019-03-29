import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models


class doubleVGG19_bn(nn.Module):
	def __init__(self, num_classes):
		super( doubleVGG19_bn, self ).__init__()

		vgg19_baseBad = models.vgg19_bn(pretrained=True)
		self.featuresBad = vgg19_baseBad.features
		self.classifierBad = vgg19_baseBad.classifier
		self.classifierBad._modules['6'] = nn.Linear(4096, 1024)
		
		vgg19_baseOrig = models.vgg19_bn(pretrained=True)
		self.featuresOrig = vgg19_baseOrig.features
		self.classifierOrig = vgg19_baseOrig.classifier
		self.classifierOrig._modules['6'] = nn.Linear(4096, 1024)
		
		self.classifier = nn.Sequential(
			nn.Linear(2048, 512),
			nn.Dropout(),
			nn.ReLU(True),
			nn.Linear(512, 1),
		)
		

	def forward(self, x):
		x1 = self.featuresBad(x[0]) #bad image
		x1 = x1.view(x1.size(0), -1)
		y1 = self.classifierBad(x1)
		x2 = self.featuresOrig(x[1]) #original image
		x2 = x2.view(x2.size(0), -1)
		y2 = self.classifierOrig(x2)

		x3 = torch.cat( (y1, y2), 1 ) #1:dimension. Batch, Color, W, H.  to split image by CWH, dim = 1.
		y = self.classifier( x3 )
		return y


