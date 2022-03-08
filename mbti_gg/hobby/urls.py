from django.urls import path
from hobby import views

urlpatterns = [
    path('', views.index, name='hobby_index'),
    path('like_btn/', views.like, name='hobby_like'),
]