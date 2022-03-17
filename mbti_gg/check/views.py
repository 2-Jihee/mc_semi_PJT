from django.shortcuts   import render, redirect
from .models            import *

# Create your views here.

def index(request) :
    print(">>>>>>>>>> check index")
    return render(request, 'check/index.html')