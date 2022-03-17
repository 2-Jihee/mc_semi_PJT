from django.shortcuts import render
from common.views import context_login, context_selected_mbti


# Create your views here.
def index(request):
    print('>>> Place - Index')

    # initialize the page
    context = {
        'title': 'Place',
        'nav_link_active': 'place',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    return render(request, 'place/index.html', context)