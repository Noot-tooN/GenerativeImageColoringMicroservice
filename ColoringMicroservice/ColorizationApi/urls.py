from django.urls import path
from .views import *

urlpatterns = [
    path('', my_view.as_view(), name="Default endpoint")
]