from django.urls import path
from . import views as v

urlpatterns = [
    path("classify/", v.classify_name, name="classify"),
]