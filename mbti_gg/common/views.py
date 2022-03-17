from django.shortcuts import redirect


# Create your views here.
def index(request):
    print('>>> Common')
    return redirect('home_index')


def context_login(context, request):
    if 'login_type' in request.session:
        if request.session['login_type'] == 'login':
            context['login_type'] = request.session['login_type']
            context['user_id'] = request.session['user_id']
            context['user_name'] = request.session['user_name']
            context['user_mbti'] = request.session['user_mbti']

    return


def context_selected_mbti(context, request):
    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
    elif 'user_mbti' in context:
        selected_mbti = context['user_mbti']
    else:
        selected_mbti = ''
    context['selected_mbti'] = selected_mbti

    return

