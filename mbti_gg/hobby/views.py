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
        liked_count = HobbyLiked.objects.values('hobby_id').annotate(Count('hobby_id'))
        # 이거 생각해보기 print로는 0 나옴. = > like_count = HobbyLiked.objects.filter(hobby_id=h_id).count()
        # print('⛔️ like check',liked_count)
        # for like in liked_count:
        #     print('⛔️ like check',like['hobby_id'],like)
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
            'liked_count' : liked_count,
        }

        return render(request, 'hobby/index.html', context)
    else:
        selected_mbti = ''
        context = {
            'selected_mbti': selected_mbti,
        }
        return render(request, 'hobby/select_mbti.html', context)
# 0을 표시하는 방법이 필요한 듯 하다...

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

def rmd_submit(request):
    print('✅ GET User Recommend Hobby Btn🚀')
    title = request.POST['title']
    user_name = request.POST['label_text']
    try:  # Hobby의 타이틀이 있다면 hobby_liked table에 좋아요를 생성
        hobby = Hobby.objects.get(title=title)
        h_id = hobby.hobby_id
        try :  # hobby_liked table에 user_id 와 hobby_id가 있을 경우
            user = User.objects.get(name=user_name)
            u_id = user.user_id
            liked = HobbyLiked.objects.get(user_id=u_id, hobby_id=h_id)
            print('⛔️ Dislike target : ', liked.user_id,liked.hobby_id.title)
            liked.delete()
            like_count = HobbyLiked.objects.filter(hobby_id=h_id).count()
            context = {
                'message': '좋아요 취소',
                'like_count': like_count
            }
            return JsonResponse(context)
        except: # hobby_liked table에 user_id 와 hobby_id가 없을 경우
            user = User.objects.get(name=user_name)
            u_id = user.user_id
            obj = HobbyLiked.objects.create(
                hobby_id=Hobby.objects.get(hobby_id=h_id),
                user_id=User.objects.get(user_id=u_id)
            )
            obj.save()
            print('⛔️ Like target : ', obj.user_id, obj.hobby_id.title)
            like_count = HobbyLiked.objects.filter(hobby_id=h_id).count()
            context = {
                'message': '좋아요',
                'like_count': like_count
            }
            return JsonResponse(context)
    except:  # hobby의 title이 일치하는게 없으면 hobby에 데이터를 추가!
        print('⛔️ DoesNotExist title')
        user = User.objects.get(name=user_name)
        user_id = user.user_id
        new_data = Hobby.objects.create(
            title=title,
            user_id = User.objects.get(user_id = user_id)
        )
        new_data.save()
        hobbys = Hobby.objects.all()
        jsonAry=[]
        for hobby in hobbys:
            if hobby.user_id.user_id != 'admin':
                jsonAry.append({
                    'title':hobby.title,
                    'user_name':hobby.user_id.name,
                    'like_count': HobbyLiked.objects.filter(hobby_id=hobby.hobby_id).count()
                })
        print(jsonAry)
        return JsonResponse(jsonAry, safe=False)
# 왜 좋아요 취소하면 다른 좋아요도 다 같이 취소될까... 근데 새로고침하면 또 안 사라져있음...
# html쪽에는 문제가 아닌 것같음... 아마 views쪽에서 잘 못 건들인것 같음...



