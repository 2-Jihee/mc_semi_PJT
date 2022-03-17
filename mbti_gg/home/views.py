from django.shortcuts import render
from common.views import context_login, context_selected_mbti


# Create your views here.
def index(request):
    print('>>> Home - Index')

    # initialize the page
    context = {
        'title': 'Home',
        'nav_link_active': 'home',
    }
    context_login(context, request)
    context_selected_mbti(context, request)
    
    return render(request, 'home/index.html', context)

