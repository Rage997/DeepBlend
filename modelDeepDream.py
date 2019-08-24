import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import argparse
import os
import tqdm
import scipy.ndimage as nd
from . utils import deprocess, preprocess, clip


class DeepDreamNN:
    def __init__(self, input_image_path):  
        # self.input_image = input_image
        
        image = Image.open(input_image_path)
        # Define the model
        network = models.vgg19(pretrained=True)
        layers = list(network.features.children())
        model = nn.Sequential(*layers[: (28)])
        # if torch.cuda.is_available:
        #     model = model.cuda()
        print(network)

        # Extract deep dream image
        dreamed_image = self.deep_dream(
            image,
            model,
            iterations=20,
            lr=0.01,
            octave_scale=1.4,
            num_octaves=10
        )

    def dream(self, image, model, iterations, lr):
        """ Updates the image to maximize outputs for n iterations """
        # Tensor = torch.cuda.FloatTensor if torch.cuda.is_available else torch.FloatTensor
        Tensor = torch.FloatTensor
        image = Variable(Tensor(image), requires_grad=True)
        for i in range(iterations):
            model.zero_grad()
            out = model(image)
            loss = out.norm()
            loss.backward()
            avg_grad = np.abs(image.grad.data.cpu().numpy()).mean()
            norm_lr = lr / avg_grad
            image.data += norm_lr * image.grad.data
            image.data = clip(image.data)
            image.grad.data.zero_()
        return image.cpu().data.numpy()


    def deep_dream(self, image, model, iterations, lr, octave_scale, num_octaves):
        """ Main deep dream method """
        image = preprocess(image).unsqueeze(0).cpu().data.numpy()

        # Extract image representations for each octave
        octaves = [image]
        for _ in range(num_octaves - 1):
            octaves.append(nd.zoom(octaves[-1], (1, 1, 1 / octave_scale, 1 / octave_scale), order=1))

        detail = np.zeros_like(octaves[-1])
        for octave, octave_base in enumerate(tqdm.tqdm(octaves[::-1], desc="Dreaming")):
            if octave > 0:
                # Upsample detail to new octave dimension
                detail = nd.zoom(detail, np.array(octave_base.shape) / np.array(detail.shape), order=1)
            # Add deep dream detail from previous octave to new base
            input_image = octave_base + detail
            # Get new deep dream image
            dreamed_image = self.dream(input_image, model, iterations, lr)
            # Extract deep dream details
            detail = dreamed_image - octave_base

        return deprocess(dreamed_image)