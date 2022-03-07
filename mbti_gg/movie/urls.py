from django.urls import path
from movie import views

urlpatterns = [
    path('', views.index, name='movie_index'),
]