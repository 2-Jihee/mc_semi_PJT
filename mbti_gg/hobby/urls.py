from django.urls import path
from hobby import views

urlpatterns = [
    path('', views.index, name='hobby_index'),
    path('like_btn/', views.like, name='hobby_like'),
    path('like_submit/', views.rmd_submit, name='like_submit'),
    path('create_cmt/', views.create_cmt, name='create_cmt')
]