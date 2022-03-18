from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Count, F
from common.views import context_login, context_selected_mbti
from .models import *
from mbti.models import *
from user.models import *


############ 모든 user는 추후 session이 들어오게되면 다 바꿀 예정
# Create your views here.
def index(request):
    print('>>> Hobby - Index')

    # initialize the page
    context = {
        'title': 'Hobby',
        'nav_link_active': 'hobby',
    }
    context_login(context, request)
    context_selected_mbti(context, request)

    if context['selected_mbti'] == '':
        return render(request, 'hobby/select_mbti.html', context)

    context['mbti_table'] = Mbti.objects.get(mbti_id=context['selected_mbti'])
    context['hobbys'] = Hobby.objects.all()
    context['likes'] = HobbyLiked.objects.all()
    context['cmts'] = HobbyComment.objects.all()

    print(context['user_name'])
    return render(request, 'hobby/index.html', context)


def like(request):
    print('✅ GET Hobby Like Btn🚀')
    pk = request.POST.get('hk', None)
    ls = Hobby.objects.get(hobby_id=pk)
    uk = request.session.get('user_id')
    hobby_like = get_object_or_404(HobbyLiked, hobby_id=ls)

    if hobby_like.like_user.filter(user_id=uk).exists():
        hobby_like.like_user.remove(uk)
        message = '좋아요 취소'
    else:
        hobby_like.like_user.add(uk)
        message = '좋아요'
    context = {
        'like_count' : hobby_like.total_like_user(),
        'message' : message
    }
    return JsonResponse(context)
    # 참조 : https://wayhome25.github.io/django/2017/06/25/django-ajax-like-button/
    # 참조 : https://jisun-rea.tistory.com/entry/Django-%EC%A2%8B%EC%95%84%EC%9A%94likes-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0

def rmd_submit(request):
    print('✅ GET User Recommend Hobby Btn🚀')
    title = request.POST['title']
    uk = request.session.get('user_id')
    try:  # Hobby의 타이틀이 있다면 hobby_liked table에 좋아요를 생성
        pk = Hobby.objects.get(title=title)
        hobby_like = get_object_or_404(HobbyLiked, hobby_id=pk)
        if hobby_like.like_user.filter(user_id=uk).exists():
            print('⛔️ Exist title')
            hobby_like.like_user.remove(uk)
            message = '좋아요 취소'
        else:
            hobby_like.like_user.add(uk)
            message = '좋아요'
        context = {
            'like_count': hobby_like.total_like_user(),
            'message': message,
            'target_id':pk.hobby_id
        }
        return JsonResponse(context)
    except:  # hobby의 title이 일치하는게 없으면 hobby에 데이터를 추가!
        print('⛔️ DoesNotExist title')
        new_data = Hobby.objects.create(
            title=title,
            user_id = User.objects.get(user_id = uk)
        )
        new_data.save()  # hobby table에 insert
        new_liked = HobbyLiked.objects.create(
            hobby_id=Hobby.objects.get(title=title)
        )
        new_liked.save()  # Hobby liked table에 insert
        hobbys = Hobby.objects.all()
        jsonAry=[]
        for hobby in hobbys:
            if hobby.user_id.user_id != 'admin':
                like = get_object_or_404(HobbyLiked, hobby_id=hobby.hobby_id)
                jsonAry.append({
                    'title':hobby.title,
                    'user_name':hobby.user_id.name,
                    'like_count': like.total_like_user(),
                    'target_id': hobby.hobby_id
                })
        return JsonResponse(jsonAry, safe=False)


def create_cmt(request):
    print('✅ GET User Comment Btn🚀')
    cmt = request.POST.get('cmt',None)
    s_mbti = request.POST.get('s_mbti',None)
    obj = HobbyComment.objects.create(
        user_id = User.objects.get(user_id=request.session.get('user_id')),
        mbti_id = Mbti.objects.get(mbti_id=s_mbti),
        comment = cmt
    )
    obj.save()
    print(obj)
    cmts = HobbyComment.objects.all()
    jsonAry = []
    for cmt in cmts:
        if cmt.mbti_id.mbti_id == s_mbti:
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
    HobbyComment.objects.get(h_cno=h_cno).delete()
    cmts = HobbyComment.objects.all()
    jsonAry = []
    for cmt in cmts:
        if cmt.mbti_id.mbti_id == s_mbti:
            jsonAry.append({
                'h_cno' : cmt.h_cno,
                'name' : cmt.user_id.name,
                'mbti': cmt.user_id.mbti_id.mbti_id,
                'cmt': cmt.comment
            })
    print(jsonAry)
    return JsonResponse(jsonAry, safe=False)