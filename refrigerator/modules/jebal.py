import os
from os import chdir
from refrigerator.models import Image


def deep_learning():

  base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #프로젝트 경로
  
  img = Image.objects.last() #방금 올린 사진의 url을 가져옴

  img_path = img.image_up.url.replace('/', '\\').split(os.path.sep) # 이미지의 url을 가져옴
  print(img_path)
  image_path = os.path.join(base_path, *img_path)
  yolo_path = os.path.join(base_path, 'yolov5')

  chdir(yolo_path)
  os.system(f'python detect.py --save-crop --source {image_path} --weights ./best.pt --img 416 --conf 0.5 --save-txt --exist-ok --project ../media/')
  chdir(base_path)

  # project=ROOT / 'runs/detect'=
  path_dir = './media/exp/labels/'
  file_list = os.listdir(path_dir)
  sorted_file_list = []
  #가장 최신의 파일을 가져오는것! 
  for file in file_list:
    file_path = path_dir + file
    gen_time = os.path.getctime(file_path)
    sorted_file_list.append((file_path, gen_time))
  last_file = max(sorted_file_list, key=lambda x: x[1])[0]
  
  # 파일 내부 정보 읽어오기
  with open(last_file, 'r', encoding='UTF8') as f:
    labeling = f.readline()
  print(labeling)
  cls = int(labeling.split()[0])
  print(cls)
  
  # for file in file_list:
  #   path_file = path_dir+file
  #   with open(path_file,'r',encoding='UTF8') as f:
  #     labeling = f.readline()
  #   print(labeling)
  # cls = int(labeling.split()[0])
  # print(cls)
  
  chdir(base_path)
  path_dir2 = 'refrigerator/static/jeryo/jeryolist.txt'
  
  with open(path_dir2, 'r') as f:
    for i in range(cls+1):
        labeling2 = f.readline()
  name=labeling2.split()[1]
  
  
  # file_list2 = os.listdir(path_dir2)
  # for file2 in file_list2:
  #   path_file2 = path_dir2+file2
  #   with open(path_file2,'r') as f:
  #     for i in range(cls+1):
  #       labeling2 = f.readline()
  # name=labeling2.split()[1]

  return name
