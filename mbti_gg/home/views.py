from django.shortcuts import render
from user.views import context_login

# Create your views here.
def index(request):
    print('>>> Home - Index')

    # initialize the page
    context = {
        'title': 'Home',
        'nav_link_active': 'home',
    }
    context_login(context, request)
    # initialize selected MBTI
    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
    elif 'user_mbti_id' in context:
        selected_mbti = context['user_mbti_id']
    else:
        selected_mbti = ''
    context['selected_mbti'] = selected_mbti
    
    return render(request, 'home/index.html', context)

