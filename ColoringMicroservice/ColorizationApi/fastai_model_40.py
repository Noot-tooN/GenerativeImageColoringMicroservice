import torch
from ColorizationApi.singleton import Singleton
from ColorizationApi.TrainedNetwork.utility_functions import load_model, build_res_unet
import os

class fastai_model_40(metaclass=Singleton):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        net_G = build_res_unet(n_input=1, n_output=2, size=256, device=device)
        net_G.load_state_dict(torch.load(os.path.join(dir_path, "Models", "res18_unet_40.pt"), map_location=device))
        self.model = load_model(os.path.join(dir_path, "Models", "fastai_model_40.pt"), net_g=net_G)