from django.urls import path
from .views import *

urlpatterns = [
    path('color_image/', color_image_view.as_view(), name="color_image")
]