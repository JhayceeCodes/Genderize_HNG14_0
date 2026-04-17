from django.urls import path
from . import views as v

urlpatterns = [
    path("profiles", v.ProfileView.as_view()),
    path("profiles/<uuid:id>", v.ProfileDetailView.as_view()),
]