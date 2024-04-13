import os
import requests
from os import chdir
from urllib.parse import urlparse

# 전역 변수로 image_path 정의
image_path = ''

def deep_learning(image_url):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 프로젝트 경로

    chdir(base_path)
    yolo_path = os.path.join(base_path, 'yolov5')

    chdir(yolo_path)
    
    # 이미지 다운로드 함수 호출 및 image_path 설정
    image_path = download_image(image_url)
    
    os.system(f'python detect.py --save-crop --source {image_path} --weights ./best.pt --img 416 --conf 0.5 --save-txt --exist-ok --project ../media/')
    chdir(base_path)

    path_dir = './media/exp/labels/'
    file_list = os.listdir(path_dir)
    sorted_file_list = []

    for file in file_list:
        file_path = os.path.join(path_dir, file)
        gen_time = os.path.getctime(file_path)
        sorted_file_list.append((file_path, gen_time))
    last_file = max(sorted_file_list, key=lambda x: x[1])[0]

    with open(last_file, 'r', encoding='UTF8') as f:
        labeling = f.readline()
    print(labeling)
    cls = int(labeling.split()[0])
    print(cls)

    chdir(base_path)
    path_dir2 = 'refrigerator/static/jeryo/jeryolist.txt'

    with open(path_dir2, 'r') as f:
        for i in range(cls + 1):
            labeling2 = f.readline()
    name = labeling2.split()[1]

    return name

# 이미지 다운로드 함수 수정
def download_image(url):
    response = requests.get(url)
    
    # 디렉토리 및 파일 이름 설정
    save_dir = './static/'  # 원하는 디렉토리로 변경하세요
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'downloaded_image.jpg')  # 수정된 부분
    
    # 이미지 저장
    with open(save_path, 'wb') as f:
        f.write(response.content)
    
    return save_path

# 이미지 다운로드
image_url = "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNDAxMDlfOTgg%2FMDAxNzA0Nzc5ODgzNTAy.TaWB8hUZ4jxW3s4vxSNgurVTn3ErRi9wTIxo4hEfloog.avvu11JQHxjju_eI9W7FMEKCOjL6iyJiasn5sfkjy-Qg.PNG.droit194%2F3.png&type=sc960_832"
result = deep_learning(image_url)
print(result)
