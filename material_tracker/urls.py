from django.urls import path

from . import views

urlpatterns = [
    # ex: api/tracker/material/
    path("material/", views.index, name="index"),
    
]