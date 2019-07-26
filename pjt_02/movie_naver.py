import requests # 요청 보내는 모듈
from pprint import pprint
from decouple import config
import time
import csv

# time.sleep(0.1) = > 요청이 너무 빨라서 오류가 발생할 때 사용 

# REST API, OPEN API 란?

BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
# Header에 담아야 되는 내용

ID = config('CLIENT_ID')
SECRET = config('CLIENT_SECRET')

# Header
# 요청은 객층으로 이루어져있다. Header, Data로 구분이 되어있음
# Header에는 요청에 대한 정보들이 담겨 있다.
HEADERS = {
    'X-Naver-Client-Id' : ID ,
    'X-Naver-Client-Secret' : SECRET, 
}

mov_Nm_list = [] # movie.csv에서 영화명(국문)을 받아올 빈 리스트, API_URL에서 query를 구성
mov_Cd_dict = {} # 최종결과이 key값이 될 영화코드를 받을 빈 dictionary, 영화명(국문)을 key값으로 한다.
mov_data = {} # 영화명(국문)으로 추출한 모든 data들을 저장할 dictionary 
mov_dir = {} # 영화명(국문) 중복으로 인해 한 번의 요청으로 여러 data가 나오는 문제를 '감독'으로 필터링 하기 위한 dictionary

with open('movie.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 영화코드를 리스트로 생성
    for row in reader:
        mov_Nm_list.append(row['영화명(국문)'])
        mov_Cd_dict[row['영화명(국문)']] = row['영화 대표코드']
        mov_dir[row['영화명(국문)']] = row['감독']



for mov_Nm in mov_Nm_list: # movie.csv에서 추출한 영화명(국문)을 query에 넣어주어 요청 보냄
    need_data = {}
    query = mov_Nm
    API_URL = f'{BASE_URL}?query={query}'
    # 요청 보내기
    response = requests.get(API_URL, headers=HEADERS).json() # 파이썬이 접근 가능한 dictionary 형태로 data를 받음
    items = response.get('items')
    
    if response['display'] == 1: # 'display' == 1이면 중복되지 않았다는 의미이므로 바로 data를 추출함
        need_data['영화코드'] = mov_Cd_dict[mov_Nm]
        need_data['네이버 영화 정보 URL'] = items[0].get('link')
        need_data['영화 썸네일 이미지'] = items[0].get('image')
        need_data['네티즌 평점'] = items[0].get('userRating')
    
    else:    
        for i in range(len(items)):
            director = items[i].get('director').split('|') # 네이버 검색 요청에서 결과가 여러개이면 '|'로 묶여있는 것을 확인하여 확실한 탐색을 위해 '|'를 기준으로 분리하였다. 
            
            for j in range(len(director)): 
                if director[j] == mov_dir[mov_Nm]: # 감독명이 일치하면 data를 추출함
                    need_data['영화코드'] = mov_Cd_dict[mov_Nm]
                    need_data['네이버 영화 정보 URL'] = items[i].get('link')
                    need_data['영화 썸네일 이미지'] = items[i].get('image')
                    need_data['네티즌 평점'] = items[i].get('userRating')
                
                else: # 감독명이 사이트에 따라 표기법이 다를 수 있으므로 이름 유사성으로 data를 추출함
                    a = list(director[j])
                    b = list(mov_dir[mov_Nm])
                    count = 0
                    for k in range(len(a)):
                        for n in range(len(b)):
                            if a[k] == b[n]:
                                count += 1
                    
                    if count/len(b) > 0.7:
                        need_data['영화코드'] = mov_Cd_dict[mov_Nm]
                        need_data['네이버 영화 정보 URL'] = items[i].get('link')
                        need_data['영화 썸네일 이미지'] = items[i].get('image')
                        need_data['네티즌 평점'] = items[i].get('userRating')            

    mov_data[mov_Cd_dict[mov_Nm]] = need_data

    time.sleep(0.1)


pprint(mov_data)

with open('movie_naver.csv', 'w', newline = '',  encoding = 'utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('영화코드', '네이버 영화 정보 URL', '영화 썸네일 이미지', '네티즌 평점', )
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    # 필드 이름을 csv파일 최상단에 작성한다.
    writer.writeheader()

    #Dictionary를 순회하며 key 값에 맞는 value 를 한줄씩 작성한다.
    for data in mov_data.values():
        writer.writerow(data)
