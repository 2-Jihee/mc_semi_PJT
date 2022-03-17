from django.shortcuts import render
from common.views import context_login, context_selected_mbti


# Create your views here.
def index(request):
    print('>>> Place - Index')

    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
    else:
        selected_mbti = ''

    context = {
        'title': 'Place',
        'nav_link_active': 'place',
        'selected_mbti': selected_mbti,
    }
    return render(request, 'place/index.html', context)