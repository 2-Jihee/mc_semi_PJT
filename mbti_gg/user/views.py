from django.shortcuts import render, redirect
from common.views import context_login, context_selected_mbti
from user.models import User


# Create your views here.
def login(request):
    print('>>> User - Login')

    # redirect if user has already logged in
    if 'login_type' in request.session:
        if request.session['login_type'] == 'login':
            return redirect('home_index')

    # initialize the page
    context = {
        'title': 'Login',
        'nav_link_active': 'user',
    }

    return render(request, 'user/login.html', context)


def login_submit(request):
    print('>>> User - Login submit')
    user_id = request.POST['user_id']
    pwd = request.POST['pwd']

    if User.objects.filter(user_id=user_id, pwd=pwd).exists():
        login_user = User.objects.get(user_id=user_id, pwd=pwd)
        print('>>> User - Login user_id:{}'.format(user_id))

        # create login session
        request.session['login_type'] = 'login'
        request.session['user_id'] = login_user.user_id
        request.session['user_name'] = login_user.name
        request.session['user_mbti'] = login_user.mbti_id.mbti_id

        return redirect('home_index')

    else:
        # incorrect id & password
        return redirect('user_login')


def logout(request):
    print('>>> User - Logout')

    request.session['login_type'] = 'logout'
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)
    request.session.pop('user_mbti_id', None)

    return redirect('home_index')


def signup(request):
    print('>>> User - Signup')
    
    # redirect if user has already logged in
    if 'login_type' in request.session:
        if request.session['login_type'] == 'login':
            return redirect('home_index')

    # initialize the page
    context = {
        'title': 'Sign Up',
        'nav_link_active': 'user',
    }

    return render(request, 'user/signup.html', context)


def signup_submit(request):
    print('>>> User - Signup submit')

    return


def info(request):
    print('>>> User - Information')

    # initialize the page
    context = {
        'title': 'User Info',
        'nav_link_active': 'user',
    }
    context_login(context, request)

    return render(request, 'user/info.html', context)




