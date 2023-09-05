import clip
import torch
import os

use_cuda = False


# 1. load the languages
# 2. make the reader class object have a check in the init for the proper class name

def test_function():
    device = 'cuda' if torch.cuda.is_available() and use_cuda else 'cpu'
    model, preprocess = clip.load("ViT-B/16", device=device)
    texts = ["a sample text", "an image of ad og"]
    texts = clip.tokenize(texts).to(device)
    print('this sample function is working i guess? here is a bunch of idk', texts.shape)
