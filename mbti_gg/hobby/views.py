from django.shortcuts import render


# Create your views here.
def index(request):
    print('>>> Hobby - Index')

    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
    else:
        selected_mbti = ''

    context = {
        'title': 'Hobby',
        'nav_link_active': 'hobby',
        'selected_mbti': selected_mbti,
    }
    return render(request, 'hobby/index.html', context)

