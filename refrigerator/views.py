from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import random
from refrigerator.modules import db_open
from django.conf import settings

    
#메인페이지
def main_page(request):
    if request.method == 'GET':
        login_user_id = request.session.get('user_id')
        login_user = User.objects.get(pk=login_user_id)
        login_user = {
            'login_user_id' : login_user_id,
            'login_user' : login_user,
        }
        return render(request,'refrigerator/main_page.html',login_user)

#회원가입
def signup(request):
    if request.method == 'GET':
        random_recipe_set = set()
        number_of_records = Recipe.objects.count()
        while len(random_recipe_set) < 5:
            random_index = int(random.random()*number_of_records)+1
            random_recipe = Recipe.objects.get(pk=random_index)
            random_recipe_set.add(random_recipe)
            
        fav_recipe_list = {
            'fav_recipe_list' : random_recipe_set
        }
        #print('총{}개 중 {} {}'.format(number_of_records, random_index, random_recipe))
        return render(request, 'refrigerator/signup.html', fav_recipe_list)
    elif request.method == 'POST':
        user_fav_recipe_list = []
        user_id = request.POST.get('user_id', None)
        user_pw = request.POST.get('user_pw', None)
        user_pw_confirm = request.POST.get('user_pw_confirm', None)
        user_name = request.POST.get('user_name', None)
        user_gender = request.POST.get('user_gender', None)
        user_recipe_id = request.POST.getlist('recipe_id[]', None)
        user_rating = request.POST.getlist('rating[]', None)
        
        for id in user_recipe_id:
            recipe = Recipe.objects.get(pk=id)
            user_fav_recipe_list.append(recipe)
        
        try:
            saved_user = User.objects.get(pk=user_id)
        except:
            saved_user = None
        
        if not(user_id and user_pw and user_pw_confirm and user_name and user_gender):
            messages.info(request, '모든 값을 입력해주세요.')
        elif saved_user != None:
            messages.info(request, '동일한 아이디가 존재합니다.')
        elif user_pw != user_pw_confirm:
            messages.info(request, '비밀번호와 비밀번호 확인 값이 일치하지 않습니다.')
        else:
            messages.info(request, '회원가입 완료!')
            user = User(user_id=user_id, user_pw=user_pw, 
                        user_name=user_name, user_gender=user_gender)
            user.save()
            #user_one = User.objects.get(pk=user_id)
            for i in range(len(user_recipe_id)):
                id = user_recipe_id[i]
                fav_recipe = Favorite_Recipe(fav_user_id=User.objects.get(pk=request.POST['user_id']),
                                             fav_recipe_id=Recipe.objects.get(pk=id), rating=user_rating[i])
                fav_recipe.save()
            print(user_recipe_id)
            print(user_rating)
            return render(request, 'refrigerator/login.html')
        print("랜덤 리스트는", user_fav_recipe_list)
        fav_recipe_list = {
            'fav_recipe_list' : user_fav_recipe_list,
            'input_user_id' : user_id,
            'input_user_pw' : user_pw,
            'input_user_pw_confirm' : user_pw_confirm,
            'input_user_name' : user_name,
            'input_user_gender' : user_gender,
        }
        return render(request, 'refrigerator/signup.html', fav_recipe_list)

#로그인
def login(request):
    if request.method =='POST':
        user_id = request.POST.get('user_id', None)
        user_pw = request.POST.get('user_pw', None)
        remember_session = request.POST.get('remember_session', False)
        if not(user_id and user_pw): 
            messages.info(request, '모든 값을 입력해주세요.')
            # return render(request, 'refrigerator/login.html', {'user':user})
        else:
            try:
                user_Set = User.objects.get(pk=user_id)
            except:
                user_Set = None
            if user_Set == None:
                messages.info(request, '일치하는 아이디가 없습니다.')
                return render(request, 'refrigerator/login.html')
            else:
                if user_id == user_Set.user_id:
                    if user_pw == user_Set.user_pw:
                        login_user = User.objects.get(pk=user_id)
                        # login = {
                        #     'login_user' : login_user
                        # }
                        request.session['user_id'] = login_user.user_id
                        return redirect('/refrigerator/main_page')
                        # return render(request, 'refrigerator/main_page.html', login)
                    else:
                        messages.warning(request, '비밀번호가 일치하지 않습니다.')
                        return render(request, 'refrigerator/login.html')
        return render(request, 'refrigerator/login.html')
    elif request.method == 'GET':
        return render(request, 'refrigerator/login.html')
#로그아웃   
def logout(request):
    request.session.clear()
    return redirect('/refrigerator')

#회원정보 수정
def user_modify(request):
    if request.method == 'POST':
        #현재 로그인된 user_id 값 가져옴
        current_user_id = request.POST.get('user_id')
        user = User.objects.get(pk=current_user_id)
        
        new_user_pw = request.POST['new_user_pw']
        user_re_pw = request.POST['renew_user_pw']
        new_user_name = request.POST['new_user_name']
        new_user_gender = request.POST['new_user_gender']
        
        user.user_id = current_user_id
        user.user_pw = new_user_pw
        user_re_pw = user_re_pw
        user.user_name = new_user_name
        user.user_gender = new_user_gender
        
        login_user = {
            'current_user_id' : current_user_id,
            'new_user_pw' : new_user_pw,
            'user_re_pw' : user_re_pw,
            'new_user_name' : new_user_name,
            'new_user_gender' : new_user_gender,
        }
        
        if not(new_user_pw and user_re_pw and new_user_name and new_user_gender):
            messages.info(request, '모든 값을 입력해주세요.')
        elif user.user_pw == user_re_pw:
            user.save()
            return redirect("/refrigerator")
        else:
            messages.info(request, '비밀번호와 비밀번호 확인 값이 일치하지 않습니다.')
        return render(request, 'refrigerator/user_modify.html', login_user)
    elif request.method == 'GET':
        #로그인 시,session에 저장된 user_id값을 이용해 현재 유저 id 값 알아옴
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id) #pk값과 id값이 같은 User모델 가져오기
        login_user = {
            'modify_login_user' : user
        }
        return render(request, 'refrigerator/user_modify.html', login_user)

#회원 탈퇴  
def user_delete(request):
    if request.method == 'GET':
        #로그인 시,session에 저장된 user_id값을 이용해 현재 유저 id 값 알아옴
        user_id = request.session.get('user_id')
        #user_id로 저장된 DB 모두 삭제하기
        user = User.objects.get(pk=user_id)
        refrigerator = Refrigerator.objects.filter(refri_user_id=user_id)
        favorite_recipe = Favorite_Recipe.objects.filter(fav_user_id=user_id)
        
        user.delete()
        refrigerator.delete()
        favorite_recipe.delete()
        return redirect("/refrigerator")    

#전체레시피 
def total_recipe(request):
    total_recipe = Recipe.objects.all()

    return render(request, 'refrigerator/total_recipe.html', {'total_recipe' : total_recipe} )

#특정 레시피의 디테일 레시피 
def detail_recipe(request, ppk):
    #특정 요리에 대한 정보만 받아올 것이므로 .all()이 아닌 .get(PK=ppk)으로 진행해야됨!!
    user_id = request.session.get('user_id')
    total_recipe = Recipe.objects.get(recipe_id=ppk)  
    context = {
        'recipe' : total_recipe,
        'user_id' : user_id
    }
    return render(request, 'refrigerator/detail_recipe.html', context)

#평점 매긴 레시피를 DB에 저장하기! 
def fav_recipe(request):
    #Favorite_Recipe 모델 가져오기
    if request.method=="POST":
        #user_id와 recipe_id 가 존재하지 않는 경우! 
        try:
            fav_recipe= Favorite_Recipe()
            fav_recipe.fav_user_id = User.objects.get(pk= request.session.get('user_id'))
            fav_recipe.fav_recipe_id = Recipe.objects.get(pk=request.POST.get('recipe_id'))
            fav_recipe.rating = request.POST.get('rating')
            fav_recipe.save()
        
        #user_id와 recipe_id 가 존재하는 경우! 값 추가 아닌 수정해주기! 
        except:
            fav_recipe.fav_user_id = User.objects.get(pk= request.session.get('user_id'))
            fav_recipe.fav_recipe_id = Recipe.objects.get(pk=request.POST.get('recipe_id'))
            fav_recipe.rating = request.POST.get('rating')
            upd_rating = Favorite_Recipe.objects.get(fav_user_id=fav_recipe.fav_user_id,fav_recipe_id=fav_recipe.fav_recipe_id)
            upd_rating.rating = fav_recipe.rating
            upd_rating.save()          

    return redirect("/refrigerator/total_recipe")  #total_recipe페이지로 이동하기!
 
        
#평점을 매긴 나의 레시피 목록을 보여줌! 
def my_recipe(request):
    user_id = request.session.get('user_id')
    #Favorite_Recipe에서 user_id별로 가져올것임! 
    my_recipe = Favorite_Recipe.objects.filter(fav_user_id=user_id)

    context = {
        'my_recipe' : my_recipe,
    }
    return render(request, 'refrigerator/my_recipe.html', context)


#추천 레시피 '머신러닝 모델' 만들기(서프라이즈)
def my_recommend_recipe(request):
    user_id = request.session.get('user_id')
    #추천 레시피 '머신러닝 모델' 만들기
    recommend_recipe_id_list = db_open.my_rec_recipe(user_id=user_id)

    recommend_title = []
    if len(recommend_recipe_id_list) > 0:
        for i in range(10):
            recommend_title.append(Recipe.objects.get(recipe_id=recommend_recipe_id_list[i]))
    
    print("로그인한 유저", user_id)
    context = {
        'recommend_recipe_title_list' : recommend_title,
        'user_id' : user_id
    }

    return render(request, 'refrigerator/reco_recipe.html', context)

#재료 추가하기(사진 업로드하는 페이지)
def image_upload(request):
    form = Image()
    if request.method == 'POST':
        img = request.FILES['image_up']
        form.image_up = img
        form.save()
        
        from refrigerator.modules import jebal
        deep_learning = jebal.deep_learning()
        
        print(deep_learning)
        
        saved_image = Image.objects.last()
        saved_url = saved_image.image_up.url.split('/')[3]
        
        context = {
            'img': saved_url,
            'food' : deep_learning
        }
        return render(request, 'refrigerator/image_result.html', context)
    elif request.method == 'GET':
        return render(request, 'refrigerator/image_upload.html')

from datetime import datetime

#나의 냉장고 안 물품들 저장> 사진찍으면 전송되는 정보
def fridge_save(request):
    if request.method == 'POST':
        fridge = Refrigerator()
        fridge.refri_user_id = User.objects.get(pk= request.session.get('user_id'))
        fridge.main_ingre = request.POST.get("food")
        fridge.expiration = datetime.today() #오늘날짜 받아오기
        fridge.save()

        user_id = fridge.refri_user_id
        saved_refri = Refrigerator.objects.filter(refri_user_id=fridge.refri_user_id)  
        context = {
            'saved_refri' : saved_refri,
            'user_id' : user_id
        }
        return render(request, 'refrigerator/Infridge.html', context)

    else :
        fridge = Refrigerator()
        fridge.refri_user_id = User.objects.get(pk= request.session.get('user_id')) 
        user_id = fridge.refri_user_id
        saved_refri = Refrigerator.objects.filter(refri_user_id=fridge.refri_user_id) 
        context = {
            'saved_refri' : saved_refri,
            'user_id' : user_id
        }  
        return render(request,'refrigerator/Infridge.html', context )

#(딥러닝)사진찍으면 전달되는 정보로 가진 레시피 
def photo_recipe(request,main_ing):
    #"가지" 라는 식재료를 가진 레시피는 다양하므로 objeccts.filter()를 사용한다! 
    total_recipe = Recipe.objects.filter(recipe_main_ingre=main_ing)
    main_ing_a = main_ing
    print("main_ing",main_ing_a)  
    
    context = {
        'recipe' : total_recipe,
        'main_ing' : main_ing_a 
    }
    return render(request, 'refrigerator/photo_recipe.html', context)