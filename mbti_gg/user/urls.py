from django.urls import path
from user import views

urlpatterns = [
    path('login', views.login, name='user:login'),
    path('login/submit', views.login_submit),
    path('logout', views.logout),
    path('signup', views.signup, name='user:signup'),
    path('signup/submit', views.signup_submit),
    path('info', views.info, name='user:info'),
]