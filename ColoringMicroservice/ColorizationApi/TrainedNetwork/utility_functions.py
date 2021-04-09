import torch
from ColorizationApi.TrainedNetwork.main_model import MainModel
from torchvision import transforms
from fastai.vision.learner import create_body
from torchvision.models.resnet import resnet18
from fastai.vision.models.unet import DynamicUnet
from PIL import Image
from skimage.color import lab2rgb
import numpy as np
from ColorizationApi.TrainedNetwork.preprocessing import make_dataloaders

def load_model(path_name, net_g=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if net_g is None:
        model = MainModel()
    else:
        model = MainModel(net_G=net_g)
    model.load_state_dict(torch.load(path_name, map_location=device))
    model.eval()
    model.train()
    model.net_G.eval()
    model.net_G.train()
    return model

def build_res_unet(n_input=1, n_output=2, size=256, device=None):
    body = create_body(resnet18, pretrained=True, n_in=n_input, cut=-2)
    net_G = DynamicUnet(body, n_output, (size, size)).to(device)
    return net_G

def color_image(paths, colorization_model):
    dataloader = make_dataloaders(paths=paths)
    data = next(iter(dataloader))

    colorization_model.model.net_G.eval()
    with torch.no_grad():
        colorization_model.model.setup_input(data)
        colorization_model.model.forward()
    # colorization_model.model.net_G.train()

    L = colorization_model.model.L
    ab = colorization_model.model.fake_color.detach()
    L = (L + 1.) * 50.
    ab = ab * 110.
    Lab = torch.cat([L, ab], dim=1).permute(0, 2, 3, 1).cpu().numpy()
    return lab2rgb(Lab[0])


# def adapt_image(path, size=256):
#     SIZE = 256
#     transformation = transforms.Resize((size, size),  Image.BICUBIC)
#     img = Image.open(path).convert("RGB")
#     img = transformation(img)
#     img = np.array(img)
#     img_lab = rgb2lab(img).astype("float32") # Converting RGB to L*a*b
#     img_lab = transforms.ToTensor()(img_lab)
#     L = img_lab[[0], ...] / 50. - 1. # Between -1 and 1
#     ab = img_lab[[1, 2], ...] / 110. # Between -1 and 1
#     return {"L": L, "ab": ab}