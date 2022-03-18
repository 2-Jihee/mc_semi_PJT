from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.db.models import Count, F
from common.views import context_login, context_selected_mbti
from .models import *
from mbti.models import Mbti
from user.models import User


def index(request):
    print('>>> Movie - Index')

    # initialize the page
    context = {
        'title': 'Movie',
        'nav_link_active': 'movie',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    if context['selected_mbti'] == '':
        return render(request, 'movie/select_mbti.html', context)

    context['mbti_table'] = Mbti.objects.get(mbti_id=context['selected_mbti'])
    context['movies'] = Movie.objects.all()
    context['likes'] = MovieLiked.objects.all()
    context['cmts'] = MovieComment.objects.filter(mbti_id=context['selected_mbti']) # 해당 mbti에 대한 댓글만 가져오도록 수정
    return render(request, 'movie/index.html', context)


# @login_required(login_url="../login") # 로그인 하지 않은 사용자가 접근하면 로그인 화면으로 이동
def like(request): ################################ 수정필요
    print('✅ GET Hobby Like Btn🚀')
    pk = request.POST.get('mk', None)
    ls = Movie.objects.get(movie_id=pk)
    uk = request.session.get('user_id')
    movie_like = get_object_or_404(MovieLiked, movie_id=ls)

    if movie_like.m_like_user.filter(user_id=uk).exists():
        movie_like.m_like_user.remove(uk)
        message = '좋아요 취소'
    else:
        movie_like.m_like_user.add(uk)
        message = '좋아요'
    context = {
        'like_count' : movie_like.total_like_user(),
        'message' : message
    }
    return JsonResponse(context)


def rmd_submit(request): ################################ 수정필요
    print('✅ GET User Recommend Movie Btn🚀')
    # print(request.session['user_id'])
    title = request.POST.get('title')
    uk = request.session.get('user_id')
    try:  # Movie의 타이틀이 있다면 movie_liked table에 좋아요를 생성
        pk = Movie.objects.get(title=title)
        movie_like = get_object_or_404(MovieLiked, movie_id=pk)
        if movie_like.m_like_user.fliter(user_id=uk).exists():
            print('⛔️ Exist title')
            movie_like.m_like_user.remove(uk)
            message = '좋아요 취소'
        else:
            movie_like.m_like_user.add(uk)
            message = '좋아요'
        context = {
            'like_count': movie_like.total_like_user(),
            'message': message,
            'target_id': pk.movie_id
        }
        return JsonResponse(context)
    except:  # movie의 title이 일치하는게 없으면 movie에 데이터를 추가!
        print('⛔️ DoesNotExist title')
        user = User.objects.get(user_id = uk)
        print(user.mbti_id.mbti_id)
        new_data = Movie.objects.create(
            title=title,
            user_id = User.objects.get(user_id = uk),
            mbti_id = Mbti.objects.get(mbti_id = user.mbti_id.mbti_id)
        )
        new_data.save()
        new_liked = MovieLiked.objects.create(
            movie_id=Movie.objects.get(title=title)
        )
        new_liked.save()
        movies = Movie.objects.all()
        jsonAry=[]
        for movie in movies:
            if movie.user_id.user_id != 'admin':
                like = get_object_or_404(MovieLiked, movie_id=movie.movie_id)
                jsonAry.append({
                    'title': movie.title,
                    'user_name': movie.user_id.name,
                    'like_count': like.total_like_user(),
                    'target_id': movie.movie_id
                })
        print(jsonAry)
        return JsonResponse(jsonAry, safe=False)


def create_cmt(request):
    print('✅ GET User Comment Btn🚀')
    cmt = request.POST.get('cmt',None)
    selected_mbti = request.POST.get('selected_mbti', None)
    obj = MovieComment.objects.create(
        user_id = User.objects.get(user_id=request.session.get('user_id')),
        mbti_id = Mbti.objects.get(mbti_id = selected_mbti),
        comment = cmt
    )
    obj.save()
    cmts = MovieComment.objects.filter(mbti_id=selected_mbti)
    jsonAry = []
    for cmt in cmts:
        jsonAry.append({
            'm_cno': cmt.m_cno,
            'name' : cmt.user_id.name,
            'mbti' : cmt.mbti_id.mbti_id,
            'cmt' : cmt.comment
        })
    return JsonResponse(jsonAry, safe=False)


def cmt_del(request):
    print('✅ GET User Comment delete Btn🚀')
    m_cno = request.POST['m_cno']
    selected_mbti = request.POST.get('selected_mbti', None)
    # print('⛔️ request check:',m_cno)
    MovieComment.objects.get(m_cno=m_cno).delete()
    cmts = MovieComment.objects.filter(mbti_id=selected_mbti)
    jsonAry = []
    for cmt in cmts:
        jsonAry.append({
            'm_cno' : cmt.m_cno,
            'name' : cmt.user_id.name,
            'mbti': cmt.mbti_id.mbti_id,
            'cmt': cmt.comment
        })
    return JsonResponse(jsonAry, safe=False)