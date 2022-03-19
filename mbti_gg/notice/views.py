from django.shortcuts import render, redirect
from common.views import context_login, context_selected_mbti
from .models import *
from user.models import *

# Create your views here.


def index(request):
    print('>>> Notice - Index')

    # initialize the page
    context = {
        'title': 'Notice',
        'nav_link_active': 'notice',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    n_boards = Notice.objects.all().order_by('-nno')
    context['n_boards'] = n_boards

    user_id = request.session.get('user_id', False)
    if user_id == 'admin':
        print('>>> Notice - admin index')
        return render(request, 'notice/admin_index.html', context)
    elif not user_id:
        # elif user_id == False와 같음
        print('>>> Notice - (none_user) index')
        return render(request, 'notice/index.html', context)
    else:
        print('>>> Notice - (user) index')
        return render(request, 'notice/index.html', context)


def writing_form(request):
    print(">>>> writing_form")
    return render(request, 'notice/writing_form.html')


def writing(request):
    print(">>>> notice writing")
    context = {
        'title': 'Writing',
        'nav_link_active': 'notice',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    title = request.POST['title']
    writer = request.POST['writer']
    content = request.POST['content']
    print('debuge - ', title, writer, content)

    notice_db = Notice(title=title, writer=writer, content=content)
    notice_db.save()

    return redirect('notice_admin_index')


def read(request):
    print('>>>> notice read')
    context = {
        'title': 'read',
        'nav_link_active': 'notice',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    nno = request.GET['nno']
    print('debuge - ', nno)

    # select
    n_board = Notice.objects.get(nno=nno)
    context['n_board'] = n_board

    # update - commit - save()
    n_board.viewcnt = n_board.viewcnt + 1
    n_board.save()

    user_id = request.session.get('user_id', False)
    if user_id == 'admin':
        print('>>> Notice - admin read')
        return render(request, 'notice/admin_read.html', context)
    elif not user_id:
        # elif user_id == False와 같음
        print('>>> Notice - (none_user) read')
        return render(request, 'notice/read.html', context)
    else:
        print('>>> Notice - (user) read')
        return render(request, 'notice/read.html', context)


def delete(request):
    print('>>>>> notice delete')
    nno = request.GET['nno']
    print('>>>>> debuge :', nno)
    # orm - delete
    n_board = Notice.objects.get(nno=nno)
    n_board.delete()

    return redirect('notice_index')


def modify(request):
    print('>>>>> notice modify')
    nno     = request.GET['nno']
    title   = request.GET['title']
    content = request.GET['content']
    print('>>>>> debuge :', nno, title, content)
    # orm - update
    n_board = Notice.objects.get(nno=nno)
    n_board.title = title
    n_board.content = content
    n_board.save()

    return redirect('notice_index')