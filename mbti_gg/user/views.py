from django.shortcuts import render, redirect
from django.contrib import messages
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

    if request.POST:
        user_id = request.POST['user_id']
        pwd = request.POST['pwd']
        if User.objects.filter(user_id=user_id).exists():
            # id exists
            login_user = User.objects.get(user_id=user_id)
            if login_user.pwd == pwd:
                print('>>> User - Login user_id:{}'.format(user_id))
                # create login session
                request.session['login_type'] = 'login'
                request.session['user_id'] = login_user.user_id
                request.session['user_name'] = login_user.name
                request.session['user_mbti'] = login_user.mbti_id.mbti_id

                messages.success(request, '{}님(ID:{}) 로그인 되었습니다.'.format(login_user.name, user_id))
                return redirect('home_index')
            else:
                # incorrect id & password
                context['user_id'] = user_id
                context['messages'] = ['비밀번호가 올바르지 않습니다.']

    return render(request, 'user/login.html', context)


def logout(request):
    print('>>> User - Logout')

    request.session['login_type'] = 'logout'
    request.session.pop('user_id', None)
    request.session.pop('user_name', None)
    request.session.pop('user_mbti', None)

    messages.success(request, '로그아웃 되었습니다.')

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

    context_messages = []
    if request.POST:
        user_id = request.POST['user_id']
        name = request.POST['name']
        pwd = request.POST['pwd']
        pwd2 = request.POST['pwd2']
        mbti_id = request.POST['mbti_id']
        gender = request.POST['gender']
        birth_dt_str = request.POST['birth_dt_str']

        create_user = True
        if user_id == '':
            print('>>> User - Signup error: user_id is missing')
            context_messages.append('ID를 입력해 주세요.')
            create_user = False
        elif User.objects.filter(user_id=user_id).exists():
            print('>>> User - Signup error: user_id exists')
            context_messages.append('다른 회원이 사용 중인 ID 입니다: {}.'.format(user_id))
            user_id = ''
            create_user = False

        if name == '':
            print('>>> User - Signup error: name is missing')
            context_messages.append('이름(별명)을 입력해 주세요.')
            create_user = False
        elif User.objects.filter(name=name).exists():
            print('>>> User - Signup error: name exists')
            context_messages.append('이미 사용 중인 이름(별명) 입니다: {}.'.format(name))
            name = ''
            create_user = False

        if pwd == '' and pwd2 == '':
            print('>>> User - Signup error: pwd is missing')
            context_messages.append('비밀번호를 입력해 주세요.')
            create_user = False
        elif pwd != pwd2:
            print('>>> User - Signup error: pwd and pwd2 do not match')
            context_messages.append('비밀번호가 일치하지 않습니다.')
            create_user = False
        elif len(pwd) < 6 or 16 < len(pwd):
            print('>>> User - Signup error: pwd is too short or long')
            context_messages.append('비밀번호는 6글자 이상, 16글자 이하만 이용 가능합니다.')
            create_user = False

        if mbti_id == '':
            print('>>> User - Signup error: mbti_id is missing')
            context_messages.append('MBTI를 선택해 주세요.')
            create_user = False
        else:
            if Mbti.objects.filter(mbti_id=mbti_id).exists():
                mbti_id_obj = Mbti.objects.get(mbti_id=mbti_id)
            else:
                print('>>> User - Signup error: mbti_id is invalid')
                context_messages.append('선택된 MBTI가 올바르지 않습니다: {}.'.format(mbti_id))
                mbti_id = ''
                create_user = False

        if gender == '':
            print('>>> User - Signup error: gender is missing')
            context_messages.append('성별을 선택해 주세요.')
            create_user = False
        elif not (gender == 'M' or gender == 'F'):
            print('>>> User - Signup error: gender is invalid')
            context_messages.append('선택된 성별이 올바르지 않습니다: {}.'.format(gender))
            gender = ''
            create_user = False

        if birth_dt_str == '':
            birth_dt = None
        else:
            try:
                birth_dt = datetime.datetime.strptime(birth_dt_str, '%Y-%m-%d')
            except:
                print('>>> User - Signup error: birth_dt format is incorrect')
                context_messages.append('생년월일이 올바르지 않습니다: {}.'.format(birth_dt_str))
                birth_dt_str = ''
                create_user = False

        if create_user:
            User(user_id=user_id, name=name, pwd=pwd, mbti_id=mbti_id_obj, gender=gender, birth_dt=birth_dt).save()

            print('>>> User - Created new user with user_id:{}'.format(user_id))
            messages.success(request, '{}님(ID:{}) 회원가입 감사드립니다.'.format(name, user_id))
            messages.success(request, '로그인해 주세요')
            return redirect('user_login')

        context['user_id'] = user_id
        context['name'] = name
        context['mbti_id'] = mbti_id
        context['gender'] = gender
        context['birth_dt_str'] = birth_dt_str

    context['messages'] = context_messages

    return render(request, 'user/signup.html', context)


def info(request):
    print('>>> User - Information')

    # redirect if user is not logged in
    if 'login_type' in request.session:
        if request.session['login_type'] != 'login':
            return redirect('user_login')

    # initialize the page
    context = {
        'title': 'User Info',
        'nav_link_active': 'user',
    }
    context_login(context, request)

    context_messages = []
    if request.POST:
        name = request.POST['name']
        curr_pwd = request.POST['curr_pwd']
        pwd = request.POST['pwd']
        pwd2 = request.POST['pwd2']
        mbti_id = request.POST['mbti_id']
        gender = request.POST['gender']
        birth_dt_str = request.POST['birth_dt_str']
        if birth_dt_str == '':
            birth_dt = None
        else:
            try:
                birth_dt = datetime.datetime.strptime(birth_dt_str, '%Y-%m-%d')
            except:
                birth_dt = None

        curr_user = User.objects.get(user_id=context['user_id'])
        if isinstance(curr_user.birth_dt, datetime.date):
            curr_birth_dt_str = curr_user.birth_dt.strftime('%Y-%m-%d')
        else:
            curr_birth_dt_str = ''

        user_info_changed = False
        input_error = False
        input_error_messages = []
        if name != curr_user.name:
            user_info_changed = True
            if name == '':
                print('>>> User - Info error: name is missing')
                input_error_messages.append('이름(별명)을 입력해 주세요.')
                input_error = True
            elif User.objects.filter(name=name).exists():
                print('>>> User - Info error: name exists')
                input_error_messages.append('다른 회원이 사용 중인 이름(별명) 입니다: {}.'.format(name))
                input_error = True
        if pwd == '' and pwd2 == '':
            pwd = curr_pwd
        else:
            user_info_changed = True
            if pwd != pwd2:
                print('>>> User - Info error: pwd and pwd2 do not match')
                input_error_messages.append('신규 비밀번호가 일치하지 않습니다.')
                input_error = True
            elif len(pwd) < 6 or 16 < len(pwd):
                print('>>> User - Info error: pwd is too short or long')
                input_error_messages.append('신규 비밀번호는 6글자 이상, 16글자 이하만 이용 가능합니다.')
                input_error = True

        if mbti_id != curr_user.mbti_id.mbti_id:
            user_info_changed = True
            if mbti_id == '':
                print('>>> User - Info error: mbti_id is missing')
                input_error_messages.append('MBTI를 선택해 주세요.')
                input_error = True
            else:
                if Mbti.objects.filter(mbti_id=mbti_id).exists():
                    mbti_id_obj = Mbti.objects.get(mbti_id=mbti_id)
                else:
                    print('>>> User - Info error: mbti_id is invalid')
                    input_error_messages.append('선택된 MBTI가 올바르지 않습니다: {}.'.format(mbti_id))
                    input_error = True
        if gender != curr_user.gender:
            user_info_changed = True
            if gender == '':
                print('>>> User - Info error: gender is missing')
                input_error_messages.append('성별을 선택해 주세요.')
                input_error = True
            elif not (gender == 'M' or gender == 'F'):
                print('>>> User - Info error: gender is invalid')
                input_error_messages.append('선택된 성별이 올바르지 않습니다: {}.'.format(gender))
                input_error = True
        if birth_dt_str != curr_birth_dt_str:
            user_info_changed = True
            if birth_dt_str != '' and birth_dt is None:
                print('>>> User - Info error: birth_dt format is incorrect')
                input_error_messages.append('생년월일이 올바르지 않습니다: {}.'.format(birth_dt_str))
                input_error = True

        if user_info_changed is False:
            print('>>> User - Info error: No change in information')
            context_messages.append('변경된 회원정보가 없습니다.')
        else:
            if curr_pwd == curr_user.pwd:
                # input pwd is correct
                if not input_error:
                    curr_user.name = name
                    curr_user.pwd = pwd
                    curr_user.mbti_id = Mbti.objects.get(mbti_id=mbti_id)
                    curr_user.gender = gender
                    curr_user.birth_dt = birth_dt
                    curr_user.save()

                    context_messages = ['{}님(ID:{}) 회원정보가 수정되었습니다.'.format(name, context['user_id'])]
                else:
                    context_messages = input_error_messages
            else:
                print('>>> User - Info error: No change in information')
                context_messages.append('입력된 비밀번호가 올바르지 않습니다.')
                context_messages = context_messages + input_error_messages

    curr_user = User.objects.get(user_id=context['user_id'])
    if isinstance(curr_user.birth_dt, datetime.date):
        curr_birth_dt_str = curr_user.birth_dt.strftime('%Y-%m-%d')
    else:
        curr_birth_dt_str = ''

    context['name'] = curr_user.name
    context['mbti_id'] = curr_user.mbti_id.mbti_id
    context['gender'] = curr_user.gender
    context['birth_dt_str'] = curr_birth_dt_str
    context['messages'] = context_messages

    return render(request, 'user/info.html', context)

