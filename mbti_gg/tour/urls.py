from django.urls import path, include
from tour import views

urlpatterns = [
    path('', views.index, name='tour_index'),
    path('like_btn/', views.like, name='tour_like'),
    path('like_submit/', views.rmd_submit, name='tour_like_submit'),
    path('create_cmt/', views.create_cmt, name='tour_create_cmt'),
    path('cmt_del/', views.cmt_del, name='tour_cmt_del')
]