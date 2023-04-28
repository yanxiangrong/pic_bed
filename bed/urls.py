from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload, name="upload"),
    path("i/<slug:name>", views.get_image, name="get image"),
    path("info/<slug:name>", views.image_info, name="image info")
]
