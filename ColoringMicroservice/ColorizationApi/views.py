from django.http import HttpResponse
from rest_framework.views import APIView
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from ColorizationApi.TrainedNetwork.utility_functions import color_image
from ColorizationApi.model_manager import model_manager
import io

def bytes_to_ndarray(bytes):
    bytes_io = bytearray(bytes)
    img = Image.open(BytesIO(bytes_io))
    return np.array(img)

class my_view(APIView):
    def post(self, request):
        permission_level = request.POST.get("permission_level", "")
        if "black-white-photo" in request.FILES:
            bw_image = request.FILES["black-white-photo"]
            bw_image = bytes_to_ndarray(bw_image.read())
            c_model = model_manager().get_model(permission_level=permission_level)
            colored_image = color_image(colorization_model=c_model, images=[bw_image])
            # it is mapped to 0 and 1, so multiply by 255 to get range from 0 to 255, because PIL needs that range
            colored_image *= 255
            jpeg_colored_image = Image.fromarray(colored_image.astype('uint8'), "RGB")
            response = HttpResponse(content_type="image/jpeg")
            jpeg_colored_image.save(response, "JPEG")
            return response
        else:
            print("No file :(")
            return HttpResponse("<h1>Angery</h1>")
