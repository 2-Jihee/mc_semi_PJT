from django.shortcuts   import render, redirect
from common.views       import context_login, context_selected_mbti
from .models            import *

# Create your views here.


def index(request) :
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

    return render(request, 'notice/index.html', context)


def writing_form(request) :
    print(">>>> writing_form")
    context = {
        'title': 'writing_form',
        'nav_link_active': 'notice',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    # user_id가 admin이면 writing_form.html로 이동
    if request.session['user_id'] == 'admin':
        return render(request, 'notice/writing_form.html', context)
    # user_id가 admin이 아니라면 notice/index.html로 이동
    elif request.session['user_id'] != 'admin':
        return redirect('notice_index')
    # 비회원 처리 어떻게?
    else:
        return redirect('notice_index')

    #return render(request, 'notice/writing_form.html', context)


def writing(request) :
    print(">>>> notice writing")
    title   = request.POST['title']
    writer  = request.POST['writer']
    content = request.POST['content']
    print('debuge - ', title, writer, content)

    notice_db = Notice(title=title, writer=writer, content=content)
    notice_db.save()

    return redirect('notice_index')


def read(request) :
    print('>>>> notice read')
    nno = request.GET['nno']
    print('debuge - ', nno)

    # select
    n_board = Notice.objects.get(nno=nno)
    # update - commit - save()
    n_board.viewcnt = n_board.viewcnt + 1
    n_board.save()

    context = {
        'title': 'read',
        'nav_link_active': 'notice',
        'n_board' : n_board
    }
    return render(request, 'notice/read.html', context)


def delete(request) :
    print('>>>>> notice delete')
    nno = request.GET['nno']
    print('>>>>> debuge :', nno)
    # orm - delete
    n_board = Notice.objects.get(nno=nno)
    n_board.delete()

    return redirect('notice_index')


def modify(request) :
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