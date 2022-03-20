from django.shortcuts import render, redirect
from common.views import context_login, context_selected_mbti
from user.models import User
from mbti.models import Mbti
import datetime


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
    
    if user_id == '':
        print('>>> User - Signup submit error: user_id is Empty')
        return redirect('user_signup')
    elif User.objects.filter(user_id=user_id).exists():
        print('>>> User - Signup submit error: user_id exists')
        return redirect('user_signup')

    if name == '':
        print('>>> User - Signup submit error: name is Empty')
        return redirect('user_signup')
    elif User.objects.filter(name=name).exists():
        print('>>> User - Signup submit error: name exists')
        return redirect('user_signup')

    if pwd == '':
        print('>>> User - Signup submit error: pwd is Empty')
        return redirect('user_signup')

    if mbti_id == '':
        print('>>> User - Signup submit error: mbti_id is Empty')
        return redirect('user_signup')
    else:
        mbti_id = Mbti.objects.get(mbti_id=mbti_id)

    if gender == '':
        print('>>> User - Signup submit error: gender is Empty')
        return redirect('user_signup')

    User(user_id=user_id, name=name, pwd=pwd, mbti_id=mbti_id, gender=gender, birth_dt=None).save()
    print('>>> User - Created user_id:{}'.format(user_id))

    new_user = User.objects.get(user_id=user_id)
    if birth_dt != '':
        try:
            birth_date = datetime.datetime.strptime(birth_dt, '%Y-%m-%d')
            new_user = User.objects.get(user_id=user_id)
            new_user.birth_dt = birth_date
            new_user.save()
        except:
            print('>>> User - Signup submit error: birth_dt format is incorrect')
            return redirect('user_signup')

    return redirect('user_login')


def info(request):
    print('>>> User - Information')

    # initialize the page
    context = {
        'title': 'User Info',
        'nav_link_active': 'user',
    }
    context_login(context, request)

    curr_user = User.objects.get(user_id=context['user_id'])
    context['user_name'] = curr_user.name
    context['user_mbti'] = curr_user.mbti_id.mbti_id
    context['user_gender'] = curr_user.gender
    if isinstance(curr_user.birth_dt, datetime.date):
        context['user_birth_dt'] = curr_user.birth_dt.strftime('%Y-%m-%d')
    else:
        context['user_birth_dt'] = ''

    return render(request, 'user/info.html', context)


def info_submit(request):
    print('>>> User - Info submit')

    return

