from django.shortcuts import render


# Create your views here.
def index(request):
    print('>>> Movie - Index')

    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
    else:
        selected_mbti = ''

    context = {
        'title': 'Movie',
        'nav_link_active': 'movie',
        'selected_mbti': selected_mbti,
    }
    return render(request, 'movie/index.html', context)