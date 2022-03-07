from django.shortcuts import render


# Create your views here.
def index(request):
    print('>>> User - Index')

    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
    else:
        selected_mbti = ''

    context = {
        'title': 'User',
        'nav_link_active': 'user',
        'selected_mbti': selected_mbti,
    }
    return render(request, 'user/index.html', context)

