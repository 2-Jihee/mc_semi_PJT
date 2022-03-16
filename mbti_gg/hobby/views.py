from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Count, F
from .models import *
from mbti.models import *
from user.models import *


############ 모든 user는 추후 session이 들어오게되면 다 바꿀 예정
# Create your views here.
def index(request):
    print('>>> Hobby - Index')
    try:
        selected_mbti = request.GET['mbti']
        hobbys = Hobby.objects.all()
        mbti_table = Mbti.objects.get(mbti_id=selected_mbti)
        likes = HobbyLiked.objects.all()
        # 0을 구성했다.. 문제는... hobbyliked에 해당 hobby_ID가 심어져야지 확인이 가능하다..
        # 그래서 다른 예시들 보면 hobby main table에 심어 놓는 이유가 이거 때문이다...
        # 이렇게 모델과 뷰를 구성하게 되면 굳이 hobby_liked table이 필요한 이유가 있을 까??
        # for like in likes:
        #     l = like.like_user.all()
        #     print('≈,l)
        #     t = like.hobby_id
        #     print('⛔️ request check:',t)
        cmts = HobbyComment.objects.all()
        user_mbti = request.session.get('user_mbti')
        user_name = request.session.get('user_name')
        context = {
            'title': 'Hobby',
            'nav_link_active': 'hobby',
            'selected_mbti': selected_mbti,
            'hobbys' : hobbys,
            'mbti_table' : mbti_table,
            'user_mbti': user_mbti,
            'user_name': user_name,
            'likes' : likes,
            'cmts' : cmts,
        }

        return render(request, 'hobby/index.html', context)
    except Exception:
        selected_mbti = ''
        context = {
            'selected_mbti': selected_mbti,
        }
        return render(request, 'hobby/select_mbti.html', context)

def like(request):
    print('✅ GET Hobby Like Btn🚀')
    pk = request.POST.get('hk', None)
    ls = Hobby.objects.get(hobby_id=pk)
    uk = request.POST.get('uk', None)
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

    # 개같이 성공했음...
    # 참조 : https://wayhome25.github.io/django/2017/06/25/django-ajax-like-button/
    # 참조 : https://jisun-rea.tistory.com/entry/Django-%EC%A2%8B%EC%95%84%EC%9A%94likes-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0

def rmd_submit(request):
    print('✅ GET User Recommend Hobby Btn🚀')
    title = request.POST['title']
    user_name = request.POST.get('label_text',None)
    try:  # Hobby의 타이틀이 있다면 hobby_liked table에 좋아요를 생성
        pk = Hobby.objects.get(title=title)
        target_id = pk.hobby_id
        user = User.objects.get(name=user_name)
        uk = user.user_id
        print('⛔️ request check:', uk, user, target_id, pk, title)
        hobby_like = get_object_or_404(HobbyLiked, hobby_id=pk)
        if hobby_like.like_user.filter(user_id=uk).exists():
            print('⛔️ Does Exist title')
            hobby_like.like_user.remove(uk)
            message = '좋아요 취소'
        else:
            hobby_like.like_user.add(uk)
            message = '좋아요'
        context = {
            'like_count': hobby_like.total_like_user(),
            'message': message,
            'target_id':target_id
        }
        return JsonResponse(context)
    except:  # hobby의 title이 일치하는게 없으면 hobby에 데이터를 추가!
        print('⛔️ DoesNotExist title')
        user = User.objects.get(name=user_name)
        uk = user.user_id
        new_data = Hobby.objects.create(
            title=title,
            user_id = User.objects.get(user_id = uk)
        )
        new_data.save()
        new_liked = HobbyLiked.objects.create(
            hobby_id=Hobby.objects.get(title=title)
        )
        new_liked.save()
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
        print(jsonAry)
        return JsonResponse(jsonAry, safe=False)
# 다 구성 완료

def create_cmt(request):
    print('✅ GET User Comment Btn🚀')
    cmt = request.POST.get('cmt',None)
    label_name = request.POST.get('label_name', None)
    user_object = User.objects.get(name=label_name)
    user_id = user_object.user_id
    #  user _ id 는 나중에 session이 나오면 바꿔질 예정
    print('⛔️ request check:',cmt, user_id)
    obj = HobbyComment.objects.create(
        user_id = User.objects.get(user_id=user_id),
        mbti_id = Mbti.objects.get(mbti_id=user_object.mbti_id.mbti_id),
        comment = cmt
    )
    # print('⛔️ request check:',obj, obj.comment, obj.user_id, obj.mbti_id)
    obj.save()
    cmts = HobbyComment.objects.all()
    jsonAry = []
    for cmt in cmts:
        jsonAry.append({
            'name' : cmt.user_id.name,
            'mbti' : cmt.mbti_id.mbti_id,
            'cmt' : cmt.comment
        })
    print(jsonAry)
    return JsonResponse(jsonAry, safe=False)