from django.urls import path
from .views import *

urlpatterns = [
    path('color_image/', my_view.as_view(), name="color_image")
]