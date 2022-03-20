from django.shortcuts import render, redirect
from common.views import context_login, context_selected_mbti
from user.models import User
from datetime import datetime


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

    if User.objects.filter(user_id=user_id, pwd=pwd).exists() is False:
        # incorrect id & password
        return redirect('user_login')

    login_user = User.objects.get(user_id=user_id, pwd=pwd)
    print('>>> User - Login user_id:{}'.format(user_id))

    # create login session
    request.session['login_type'] = 'login'
    request.session['user_id'] = login_user.user_id
    request.session['user_name'] = login_user.name
    request.session['user_mbti'] = login_user.mbti_id.mbti_id

    return redirect('home_index')


def logout(request):
    print('>>> User - Logout')

    request.session['login_type'] = 'logout'
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)
    request.session.pop('user_mbti', None)

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
        'nav_link_active': 'signup',
    }

    return render(request, 'user/signup.html', context)


def signup_submit(request):
    print('>>> User - Signup submit')

    user_id = request.POST['user_id']
    name = request.POST['name']
    pwd = request.POST['pwd']
    mbti_id = request.POST['mbti_id']
    gender = request.POST['gender']
    birth_dt = request.POST['birth_dt']

    print('>>> User - Signup try user_id:{}'.format(user_id))

    if User.objects.filter(user_id=user_id).exists():
        print('>>> User - Signup submit error: user_id exists')
        return redirect('user_login')

    if User.objects.filter(name=name).exists():
        print('>>> User - Signup submit error: name exists')
        return redirect('user_login')

    if user_id == '':
        print('>>> User - Signup submit error: user_id is Empty')
        return redirect('user_login')

    if name == '':
        print('>>> User - Signup submit error: name is Empty')
        return redirect('user_login')

    if pwd == '':
        print('>>> User - Signup submit error: pwd is Empty')
        return redirect('user_login')

    if mbti_id == '':
        print('>>> User - Signup submit error: mbti_id is Empty')
        return redirect('user_login')

    if gender == '':
        print('>>> User - Signup submit error: gender is Empty')
        return redirect('user_login')

    if birth_dt != '':
        try:
            datetime.strptime(birth_dt, '%Y-%m-%d')
        except:
            print('>>> User - Signup submit error: birth_dt format is incorrect')
            return redirect('user_login')

    User(user_id=user_id, name=name, pwd=pwd, mbti_id=mbti_id, gender=gender, birth_dt=birth_dt).save()
    print('>>> User - Signup successful user_id:{}'.format(user_id))

    return redirect('user_login')


def info(request):
    print('>>> User - Information')

    # initialize the page
    context = {
        'title': 'User Info',
        'nav_link_active': 'user',
    }
    context_login(context, request)

    return render(request, 'user/info.html', context)




