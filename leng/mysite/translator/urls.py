from django.urls import path
from . import views
import os

urlpatterns = [

    path("translate", views.translate_app,name="trans"),
    path("upload", views.upload, name="upload"),
    path("menu", views.upload, name="menu"),
    path("",views.index , name="check")


]

