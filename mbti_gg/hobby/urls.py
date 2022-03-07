from django.urls import path
from hobby import views

urlpatterns = [
    path('', views.index, name='hobby_index'),
]