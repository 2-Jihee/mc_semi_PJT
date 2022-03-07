from django.urls import path
from place import views

urlpatterns = [
    path('', views.index, name='place_index'),
]