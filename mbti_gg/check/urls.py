from django.urls import path
from check       import views

urlpatterns = [
    path('',                 views.index,          name='check_index'),
]