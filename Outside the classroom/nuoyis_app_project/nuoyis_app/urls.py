from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import os
from . import views


def generate_api_paths(directory):
    paths = []
    for folder in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, folder)):
            paths.append(path(folder + '/', views.api_view, name=folder))
    return paths


urlpatterns = [
                  path("", views.index, name="index"),
                  path("jiekou.json", views.jiekou, name="jiekou")
              ] + generate_api_paths('api/')
