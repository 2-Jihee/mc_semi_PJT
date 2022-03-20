from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from common.views import context_login, context_selected_mbti
from .models import *
from mbti.models import *
from user.models import *


# Create your views here.
def index(request):
    print('>>> Tour - Index')

    # initialize the page
    context = {
        'title': 'Tour',
        'nav_link_active': 'tour',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    if context['selected_mbti'] == '':
        return render(request, 'tour/select_mbti.html', context)

    context['mbti_table'] = Mbti.objects.get(mbti_id=context['selected_mbti'])
    context['tours'] = Tour.objects.all()
    context['likes'] = TourLiked.objects.all()
    context['cmts'] = TourComment.objects.all()

    return render(request, 'tour/index.html', context)


def like(request):
    print('✅ GET Tour Like Btn🚀')
    pk = request.POST.get('hk', None)
    ls = Tour.objects.get(tour_id=pk)
    uk = request.session.get('user_id')
    tour_like = get_object_or_404(TourLiked, tour_id=ls)

    if tour_like.like_user.filter(user_id=uk).exists():
        tour_like.like_user.remove(uk)
        message = '좋아요 취소'
    else:
        tour_like.like_user.add(uk)
        message = '좋아요'
    context = {
        'like_count' : tour_like.total_like_user(),
        'message' : message
    }
    return JsonResponse(context)
    # 참조 : https://wayhome25.github.io/django/2017/06/25/django-ajax-like-button/
    # 참조 : https://jisun-rea.tistory.com/entry/Django-%EC%A2%8B%EC%95%84%EC%9A%94likes-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0

def rmd_submit(request):
    print('✅ GET User Recommend Tour Btn🚀')
    title = request.POST['title']
    print('⛔️request check : ',title)
    uk = request.session.get('user_id')
    try:  # Tour의 타이틀이 있다면 tour_liked table에 좋아요를 생성
        pk = Tour.objects.get(title=title)
        print('⛔️request check : ',pk)
        tour_like = get_object_or_404(TourLiked, tour_id=pk)
        if tour_like.like_user.filter(user_id=uk).exists():
            print('⛔️ Exist title')
            tour_like.like_user.remove(uk)
            message = '좋아요 취소'
        else:
            tour_like.like_user.add(uk)
            message = '좋아요'
        context = {
            'like_count': tour_like.total_like_user(),
            'message': message,
            'target_id':pk.tour_id
        }
        return JsonResponse(context)
    except:  # tour의 title이 일치하는게 없으면 tour에 데이터를 추가!
        print('⛔️ DoesNotExist title')
        new_data = Tour.objects.create(
            title=title,
            user_id = User.objects.get(user_id = uk),
            mbti_id = Mbti.objects.get(mbti_id = request.session.get('user_mbti'))
        )
        new_data.save()  # tour table에 insert
        new_liked = TourLiked.objects.create(
            tour_id=Tour.objects.get(title=title)
        )
        new_liked.save()  # Tour liked table에 insert
        tours = Tour.objects.all()
        s_mbti = request.POST.get('s_mbti', None)
        jsonAry=[]
        for tour in tours:
            if tour.user_id.user_id != 'admin' and tour.mbti_id.mbti_id == s_mbti:
                like = get_object_or_404(TourLiked, tour_id=tour.tour_id)
                jsonAry.append({
                    'title':tour.title,
                    'user_name':tour.user_id.name,
                    'like_count': like.total_like_user(),
                    'target_id': tour.tour_id
                })
        return JsonResponse(jsonAry, safe=False)


def create_cmt(request):
    print('✅ GET User Comment Btn🚀')
    cmt = request.POST.get('cmt',None)
    s_mbti = request.POST.get('s_mbti',None)
    obj = TourComment.objects.create(
        user_id = User.objects.get(user_id=request.session.get('user_id')),
        mbti_id = Mbti.objects.get(mbti_id=s_mbti),
        comment = cmt
    )
    obj.save()
    print(obj)
    cmts = TourComment.objects.filter(mbti_id=s_mbti)
    jsonAry = []
    for cmt in cmts:
        jsonAry.append({
            'h_cno' : cmt.h_cno,
            'name' : cmt.user_id.name,
            'mbti' : cmt.user_id.mbti_id.mbti_id,
            'cmt' : cmt.comment
        })
    return JsonResponse(jsonAry, safe=False)


def cmt_del(request):
    print('✅ GET User Comment delete Btn🚀')
    h_cno = request.POST['h_cno']
    s_mbti = request.POST.get('s_mbti',None)
    TourComment.objects.get(h_cno=h_cno).delete()
    cmts = TourComment.objects.filter(mbti_id=s_mbti)
    jsonAry = []
    for cmt in cmts:
        jsonAry.append({
            'h_cno' : cmt.h_cno,
            'name' : cmt.user_id.name,
            'mbti': cmt.user_id.mbti_id.mbti_id,
            'cmt': cmt.comment
        })
    print(jsonAry)
    return JsonResponse(jsonAry, safe=False)