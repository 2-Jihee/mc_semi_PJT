from django.shortcuts import redirect


# Create your views here.
def index(request):
    print('>>> Common')
    return redirect('home_index')

