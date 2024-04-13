from django.shortcuts import render
import pandas as pd
from refrigerator.models import Recipe, Favorite_Recipe
from surprise import Dataset, SVD, Reader

def my_rec_recipe(user_id):
    #추천 레시피 '머신러닝 모델' 만들기
    fav_data = Favorite_Recipe.objects.all().values_list('fav_user_id','fav_recipe_id','rating')
    fav_recipe_id_list=[] #fav_recipe_id 리스트
    fav_user_id_list=[]
    rating_list=[]
    for i in range(len(fav_data)):
        fav_user_id_list.append(list(fav_data[i])[0])
        fav_recipe_id_list.append(list(fav_data[i])[1])
        rating_list.append(list(fav_data[i])[2])
    data = { 'fav_user_id' : fav_user_id_list, 'fav_recipe_id' : fav_recipe_id_list, 'rating': rating_list}    
    # fav_user_id / fav_recipe_id/ rating 데이터 프레임 생성 완료 
    data_df = pd.DataFrame(data, columns=['fav_user_id','fav_recipe_id','rating'])
    print(data_df)
    
    #전체 레시피 id 가져오기
    recipe_data = Recipe.objects.all().values_list('recipe_id', flat=True)
    total_recipe_id_list = []
    for i in range(len(recipe_data)):
        total_recipe_id_list.append(recipe_data[i])
    print(total_recipe_id_list)
    
    #전체 레시피 중 특정 User가 보지 못한 레시피_id : unrate_recipe_id 
    data_user_list = data_df[data_df['fav_user_id']==user_id]['fav_recipe_id'].to_list()
    print(data_user_list)
    unrate_recipe_id = list(set(total_recipe_id_list)-set(data_user_list))
    #print(type(unrate_recipe_id[0]))
    print(unrate_recipe_id)
    

    reader = Reader(rating_scale=(1,5))
    data = Dataset.load_from_df(df=data_df, reader=reader)
    
    train = data.build_full_trainset()
    
    model = SVD(n_factors=100, n_epochs=30, random_state=42)
    model.fit(train)
    
    rec_user_id = user_id
    rec_recipe_id = unrate_recipe_id
    actual_rating = 0
    
    model_pre = []
    for rec_recipe_i in rec_recipe_id:
        model_pre.append(model.predict(rec_user_id, rec_recipe_i, actual_rating))
    
    def sortkey_est(pred):
        return pred.est

    model_pre.sort(key=sortkey_est, reverse=True)
    
    recommend_recipe_id_list=[] #추천 레시피 아이디 리스트
    print(model_pre)
    print(len(model_pre))
    if len(model_pre) > 0:    
        for i in range(10):
            recommend_recipe_id_list.append(model_pre[i].iid)

    return recommend_recipe_id_list
