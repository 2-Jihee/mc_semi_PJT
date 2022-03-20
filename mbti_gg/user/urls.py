from django.urls import path
from user import views

urlpatterns = [
    path('login', views.login, name='user_login'),
    path('logout', views.logout),
    path('signup', views.signup, name='user_signup'),
    path('info', views.info, name='user_info'),
]