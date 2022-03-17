import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.db.models import Count, F
from common.views import context_login, context_selected_mbti
from .models import *
from mbti.models import Mbti
from user.models import User

################# 홈페이지 추천 조회, 회원 추천 조회, 댓글 조회, 회원 추천 입력 ,
################# 댓글 달기 및 조회, 추천 좋아요 기능(은 아마 html에서 ajax로)

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

    context['mbti_table'] = Mbti.objects.get(mbti_id=context['selected_mbti'])  # .filter()은 쿼리셋으로, get은 객체로 받아옴
    context['movies'] = Movie.objects.all() # 모든 영화 받아오기
    context['cmts'] = MovieComment.objects.all() # 모든 댓글 받아오기
    context['liked_count'] = MovieLiked.objects.values('movie_id').annotate(movie_count=Count('movie_id')).order_by('-movie_count')[:10] # Class.objects.values('col_name').annotate(nickname=Count('col_name')) # 내림차순, 상위 10개

    return render(request, 'movie/index.html', context)


# @login_required(login_url="../login") # 로그인 하지 않은 사용자가 접근하면 로그인 화면으로 이동
def like(request):
    print('✅ GET Movie Like Btn🚀')
    mk = request.POST['mk']
    uk = request.POST['uk']
    try:
        liked=MovieLiked.objects.get(user_id=uk,movie_id=mk)
        liked.delete()
        like_count = MovieLiked.objects.filter(movie_id=mk).count()
        context = {
            'message' : '좋아요 취소',
            'like_count' : like_count
        }
        return JsonResponse(context)
    except MovieLiked.DoesNotExist:
        obj = MovieLiked.objects.create(
            movie_id = Movie.objects.get(movie_id=int(mk)),
            user_id = User.objects.get(user_id=uk)
        )
        obj.save()
        like_count = MovieLiked.objects.filter(movie_id=mk).count()
        context = {
            'message' : '좋아요',
            'like_count' : like_count
        }
        return JsonResponse(context)

def rmd_submit(request):
    print('✅ GET User Recommend Movie Btn🚀')
    title = request.POST['title']
    user_name = request.POST['label_text']
    try:  # Movie의 타이틀이 있다면 movie_liked table에 좋아요를 생성
        movie = Movie.objects.get(title=title)
        m_id = movie.movie_id
        try :  # movie_liked table에 user_id 와 movie_id가 있을 경우
            user = User.objects.get(name=user_name)
            u_id = user.user_id
            liked = MovieLiked.objects.get(user_id=u_id, movie_id=m_id)
            print('⛔️ Dislike target : ', liked.user_id,liked.movie_id.title)
            liked.delete()
            like_count = MovieLiked.objects.filter(movie_id=m_id).count()
            context = {
                'message': '좋아요 취소',
                'like_count': like_count
            }
            return JsonResponse(context)
        except: # hobby_liked table에 user_id 와 hobby_id가 없을 경우
            user = User.objects.get(name=user_name)
            u_id = user.user_id

            obj = MovieLiked.objects.create(
                movie_id=Movie.objects.get(movie_id=m_id),
                user_id=User.objects.get(user_id=u_id),
            )
            obj.save()
            print('⛔️ Like target : ', obj.user_id, obj.movie_id.title)
            like_count = MovieLiked.objects.filter(movie_id=m_id).count()
            context = {
                'message': '좋아요',
                'like_count': like_count
            }
            return JsonResponse(context)
    except:  # movie의 title이 일치하는게 없으면 movie에 데이터를 추가!
        print('⛔️ DoesNotExist title')
        user = User.objects.get(name=user_name)
        user_id = user.user_id
        mbti_id = user.mbti_id
        new_data = Movie.objects.create(
            title = title,
            user_id = User.objects.get(user_id = user_id),
            mbti_id = mbti_id
        )
        new_data.save()
        movies = Movie.objects.all()
        jsonAry=[]
        for movie in movies:
            if movie.user_id.user_id != 'admin':
                jsonAry.append({
                    'title': movie.title,
                    'user_name':movie.user_id.name,
                    'like_count': MovieLiked.objects.filter(movie_id=movie.movie_id).count()
                })
        print(jsonAry)
        return JsonResponse(jsonAry, safe=False)
# 왜 좋아요 취소하면 다른 좋아요도 다 같이 취소될까... 근데 새로고침하면 또 안 사라져있음...
# html쪽에는 문제가 아닌 것같음... 아마 views쪽에서 잘 못 건들인것 같음...


# @login_required(login_url="../../login")
def create_cmt(request):
    print('>>> Movie - 회원 댓글 달기 호출')
    selected_mbti = request.POST.get('selected_mbti')
    print('>>>>> selected_mbti: ', selected_mbti) # 이건 왜 못받는걸까............
    body = request.POST.get('body')
    print('>>>>> 작성한 댓글 내용: ', body) # body는 받아오는데
    # comment = MovieComment()
    # comment.body = request.POST.get('body')
    # comment.mbti_id = get_object_or_404(Mbti, pk=request.POST.get('selected_mbti'))
    # comment.user_id = get_object_or_404(User, pk=request.POST.get(user_id = 'user3')) # 로그인 세션 생기면 'user_id'로 수정
    # comment.save()
    obj = MovieComment.objects.create(
        mbti_id = Mbti.objects.get(mbti_id = 'selected_mbti'),
        user_id = User.objects.get(user_id='user3'), # 로그인 세션 생기면 수정
        comment = body
    )
    obj.save()

    context = {
        'message' : '댓글 작성 완료',
        'body': body
    }
    # return JsonResponse(context)
    return HttpResponse(json.dumps(context), content_type="application/json") # context 변수를 json으로.. 걍 JsonResponse 하면 안되나