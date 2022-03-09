from django.urls import path
from notice      import views

urlpatterns = [
    path('',                 views.index,          name='notice_index'),
    path('writing_form/',    views.writing_form,   name='notice_writing_form'),
    path('notice_writing/',  views.writing,        name='notice_writing'),
    path('notice_read/',     views.read,           name='notice_read'),
    path('notice_delete/',   views.delete,         name='notice_delete'),
    path('notice_modify/',   views.modify,         name='notice_modify'),
]