from django.urls import path
from mbti import views

urlpatterns = [
    path('', views.index, name='mbti_index'),
]