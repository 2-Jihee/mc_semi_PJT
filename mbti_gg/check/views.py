from django.shortcuts import render, redirect
from common.views import context_login, context_selected_mbti


# Create your views here.
def index(request):
    print('>>> Check - Index')

    # initialize the page
    context = {
        'title': 'MBTI Check',
        'nav_link_active': 'check',
    }
    context_login(context, request)
    context_selected_mbti(context, request)
    
    return render(request, 'check/index.html', context)

