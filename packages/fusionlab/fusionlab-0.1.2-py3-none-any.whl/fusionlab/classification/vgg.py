# VGG Classifier
import torch
from torch import nn
from fusionlab.classification.base import CNNClassification
from fusionlab.encoders import VGG16, VGG19
from fusionlab.layers import AdaptiveAvgPool

class VGG16Classifier(CNNClassification):
    def __init__(self, spatial_dims, cin, cout):
        super().__init__()
        self.encoder = VGG16(spatial_dims, cin) # Create VGG16 instance
        self.globalpooling = AdaptiveAvgPool(spatial_dims, 1)
        self.head = nn.Linear(512, cout)

class VGG19Classifier(CNNClassification):
    def __init__(self, spatial_dims, cin, cout):
        super().__init__()
        self.encoder = VGG19(spatial_dims, cin) # Create VGG16 instance
        self.globalpooling = AdaptiveAvgPool(spatial_dims, 1)
        self.head = nn.Linear(512, cout)


if __name__ == '__main__':
    inputs = torch.randn(1, 224, 3) # create random input tensor
    model = VGG16Classifier(spatial_dims=1, cin=3, cout=2) # create model instance
    outputs = model(inputs) # pass input through model
    assert list(outputs.shape) == [1, 2] # check output shape is correct

    inputs = torch.randn(1, 224, 3) # create random input tensor
    model = VGG19Classifier(spatial_dims=1,cin=3, cout=2) # create model instance
    outputs = model(inputs) # pass input through model
    assert list(outputs.shape) == [1, 2] # check output shape is correct