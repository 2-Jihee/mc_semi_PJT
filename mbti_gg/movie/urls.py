from django.urls import path, include
from movie import views

urlpatterns = [
    # http://127.0.0.1:8000/movie/
    path('', views.index, name='movie_index'),
    path('like_btn/', views.like, name='movie_like'),
    path('like_submit/', views.rmd_submit, name='movie_like_submit'),
    path('create_cmt/', views.create_cmt, name='movie_create_cmt'),
    path('cmt_del/', views.cmt_del, name='movie_cmt_del'),

]