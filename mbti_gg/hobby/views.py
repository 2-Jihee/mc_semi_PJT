from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
from django.db.models import Count, F
from .models import *
from mbti.models import *
from user.models import *

# Create your views here.
def index(request):
    print('>>> Hobby - Index')
    if 'mbti' in request.GET:
        selected_mbti = request.GET['mbti']
        hobbys = Hobby.objects.all()
        mbti_table = Mbti.objects.get(mbti_id=selected_mbti)
        # hobby_all = Hobby.objects.select_related('user_id').all()
        # print('⛔️ request check', hobby_all)
        # print('⛔️ request check', hobbys)
        # for hobby in hobby_all:
        #     print(hobby.user_id.name)
        liked_count = HobbyLiked.objects.values('hobby_id').annotate(hobby_count=Count('hobby_id')).order_by('-hobby_count')
        # print('⛔️ like check',liked_count)
        # for like in liked_count:
        #     print('⛔️ like check',like['hobby_id'],like['hobby_count'])
        user_mbti=request.session.get('user_mbti')
        user_name=request.session.get('user_name')
        context = {
            'title': 'Hobby',
            'nav_link_active': 'hobby',
            'selected_mbti': selected_mbti,
            'hobbys' : hobbys,
            'mbti_table' : mbti_table,
            'user_mbti': user_mbti,
            'user_name': user_name,
            'liked_count' : liked_count,
        }

        return render(request, 'hobby/index.html', context)
    else:
        selected_mbti = ''
        context = {
            'selected_mbti': selected_mbti,
        }
        return render(request, 'hobby/select_mbti.html', context)


def like(request):
    print('✅ GET Hobby Like Btn🚀')
    hk = request.POST['hk']
    uk = request.POST['uk']
    try:
        liked=HobbyLiked.objects.get(user_id=uk,hobby_id=hk)
        liked.delete()
        like_count = HobbyLiked.objects.filter(hobby_id=hk).count()
        context = {
            'message' : '좋아요 취소',
            'like_count' : like_count
        }
        return JsonResponse(context)
    except HobbyLiked.DoesNotExist:
        obj = HobbyLiked.objects.create(
            hobby_id = Hobby.objects.get(hobby_id=int(hk)),
            user_id = User.objects.get(user_id=uk)
        )
        obj.save()
        like_count = HobbyLiked.objects.filter(hobby_id=hk).count()
        context = {
            'message' : '좋아요',
            'like_count' : like_count
        }
        return JsonResponse(context)
    # 개같이 성공했음...
    # 참조 : https://wayhome25.github.io/django/2017/06/25/django-ajax-like-button/
    # 참조 : https://jisun-rea.tistory.com/entry/Django-%EC%A2%8B%EC%95%84%EC%9A%94likes-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0