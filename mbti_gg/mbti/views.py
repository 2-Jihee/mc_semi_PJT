from django.shortcuts import render
from common.views import context_login, context_selected_mbti


# Create your views here.
def index(request):
    print('>>> MBTI - Index')

    # initialize the page
    context = {
        'title': 'MBTI',
        'nav_link_active': 'mbti',
    }
    context_login(context, request)
    context_selected_mbti(context, request)
    
    return render(request, 'mbti/index.html', context)

