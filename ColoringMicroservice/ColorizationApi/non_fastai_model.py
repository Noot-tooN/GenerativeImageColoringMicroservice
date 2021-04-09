from ColorizationApi.singleton import Singleton
from ColorizationApi.TrainedNetwork.utility_functions import load_model
import os

class non_fastai_model(metaclass=Singleton):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.model = load_model(os.path.join(dir_path, "Models", "non_fastai_model.pt"))