from django.test import TestCase
from ColorizationApi.model_manager import model_manager
from ColorizationApi.TrainedNetwork.utility_functions import color_image
import os
import torch
import matplotlib.pyplot as plt
from ColorizationApi.TrainedNetwork.preprocessing import make_dataloaders

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class ColorizationTestCase(TestCase):
    def setUp(self):
        self.model_manager = model_manager()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_permission_levels(self):
        current_model = self.model_manager.get_model(permission_level=2)
        class_name = type(current_model).__name__
        self.assertEqual("fastai_model_40", class_name)

        current_model = self.model_manager.get_model(permission_level=1)
        class_name = type(current_model).__name__
        self.assertEqual("fastai_model_20", class_name)

        current_model = self.model_manager.get_model(permission_level=0)
        class_name = type(current_model).__name__
        self.assertEqual("non_fastai_model", class_name)

        current_model = self.model_manager.get_model(permission_level=99)
        class_name = type(current_model).__name__
        self.assertEqual("non_fastai_model", class_name)
    
    def test_image_resize(self):
        # a_img = adapt_image(path=os.path.join(self.dir_path, "sample_test_photo.jpg"), size=256)
        test_image_path = os.path.join(self.dir_path, "sample_test_photo.jpg")
        dataloader = make_dataloaders(paths=[test_image_path])
        data = next(iter(dataloader))
        # [0] because data can work with array of pictures
        self.assertEqual(torch.Size([1, 256, 256]), data["L"][0].shape)
        self.assertEqual(torch.Size([2, 256, 256]), data["ab"][0].shape)

    def test_image_colorization(self):
        # Getting test image path
        img_path = os.path.join(self.dir_path, "sample_test_photo.jpg")
        # Getting model
        cur_model = self.model_manager.get_model(permission_level=2)
        # Coloring Test image
        resulting_image = color_image(paths=[img_path], colorization_model=cur_model)
        self.assertEqual(torch.Size([256, 256, 3]), resulting_image.shape)

        cur_model = self.model_manager.get_model(permission_level=1)
        resulting_image2 = color_image(paths=[img_path], colorization_model=cur_model)
        self.assertEqual(torch.Size([256, 256, 3]), resulting_image2.shape)

        cur_model = self.model_manager.get_model()
        resulting_image3 = color_image(paths=[img_path], colorization_model=cur_model)
        self.assertEqual(torch.Size([256, 256, 3]), resulting_image3.shape)
        # plt.imsave(os.path.join(self.dir_path, "resulting_image.jpg"), resulting_image)

class ColorizationApiTestCase(APITestCase):
    def test_image_coloring_consistency(self):
        def save_image(permission):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            url = reverse("color_image")
            f1 = open(os.path.join(dir_path, "sample_test_photo.jpg"), 'rb')
            data = {'black-white-photo': f1, "permission_level": permission}
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 200)
            f1.close()
            with open(os.path.join(dir_path, "received_perm_{}.jpg".format(permission)), 'wb') as f2:
                f2.write(response.content)

        def check_image(permission):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            url = reverse("color_image")
            f1 = open(os.path.join(dir_path, "sample_test_photo.jpg"), 'rb')
            data = {'black-white-photo': f1, "permission_level": permission}
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, 200)
            f1.close()
            # Saved images have different bytes depending if they were saved using docker or non docker env
            # So tests will fail if you dont use docker env
            # with open(os.path.join(dir_path, "received_perm_{}.jpg".format(permission)), 'wb') as f2:
            #     f2.write(response.content)
            with open(os.path.join(dir_path, "received_perm_{}.jpg".format(permission)), 'rb') as f2:
                self.assertEqual(f2.read(), response.content)
        
        save_image(0)
        check_image(0)
        save_image(1)
        check_image(1)
        save_image(2)
        check_image(2)