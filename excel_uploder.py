#csv파일에 저장된 레시피.csv 파일 DB에 저장하는 페이지
import os
from openpyxl import load_workbook
import django


#환경변수 세팅(뒷부분은 프로젝트명.settings로 설정한다.)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

#model import하기 
from refrigerator.models import Recipe

#읽어드릴 엑셀 정의하기
wb = load_workbook('./recipe.xlsx')
#C:/Users/YSJ/0_project/myrefrigerator/myrefrigerator/recipe.xlsx
sheet1 = wb['recipe']
rows= sheet1['A2':'G265'] #recipe시트의 A1 ~ G1까지 rows 변수에 할당

for row in rows:
    dict = {}
    dict['recipe_title'] = row[0].value
    dict['recipe_main_ingre'] = row[1].value
    dict['recipe_serving'] = row[2].value
    dict['recipe_time'] = row[3].value
    dict['recipe_total_ingre'] = row[4].value
    dict['recipe_order'] = row[5].value
    dict['recipe_image'] = row[6].value
    
    Recipe(**dict).save()