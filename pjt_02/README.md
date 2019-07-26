# PJT2

## 문제1

### 프로젝트의 목적 설정

- 이전에 조사한 50주 간의 TOP10 영화들의 추가적인 영화정보를 추가
- 추가할 정보는 타 사이트의 영화정보 link, 영화 썸네일 이미지, 유저 평점을 설정
- 새로운 결과를 movie_'사이트 명'.csv에 저장



#### 정보를 받아올 사이트 설정

```python
# 검색을 위한 포털을 '네이버'로 선택
# 'https://developers.naver.com/docs/search/movie/' 사이트를 통해 API 요청하는 방법을 확인
```

#### 정보 요청 방법

```python
# 아래의 URL을 통해 파이썬이 접근 가능한 json 타입으로 요청
# 요청을 위해 필수적으로 Client_Id, Client_Secret, query가 필요함을 확인
BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
```

```python
'''
출력 type을 확인하기 위한 코드
'''
# 아래와 같이 CLIENT 정보는 숨김
ID = config('CLIENT_ID')
SECRET = config('CLIENT_SECRET')
# 아래와 같이 필수적인 요청변수들을 구성하고 요청을 보냄
HEADERS = {
    'X-Naver-Client-Id' : ID ,
    'X-Naver-Client-Secret' : SECRET, 
}
query = '자전차왕 엄복동'
API_URL = f'{BASE_URL}?query={query}'
response = requests.get(API_URL, headers=HEADERS).json()
```

```python
'''
위 코드를 통해 결과의 형태를 확인
{'display': 1,
 'items': [{'actor': '비|강소라|이범수|',
            'director': '김유성|',
            'image': 'https://ssl.pstatic.net/imgmovie/mdi/mit110/1590/159070_P13_114738.jpg',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=159070',
            'pubDate': '2018',
            'subtitle': 'Race to Freedom : Um Bok Dong',
            'title': '<b>자전차왕 엄복동</b>',
            'userRating': '3.84'}],
 'lastBuildDate': 'Fri, 26 Jul 2019 10:21:37 +0900',
 'start': 1,
 'total': 1}
'''
```

#### 코드 구성 구상 및  구현

```python
# 위 결과를 통해 요청의 결과가 {'displays': dis_val, 'items': [{item_dictionary}], 'lastBuildDate': Date_val, 'start': start_val, 'total': tatal_val}로 나오는 것을 확인
# movie.csv에서 추출한 영화명(국문)을 매개로 반복문을 사용하여 모든 영화에 대한 data 요청
# 목적에 맞춰 위 결과에서 items_dictionary 중 link, image, userRating만 추출
# 이전에 만들었던 movie.csv에서 추출한 movie code를 key값으로 위의 data들을 value로 갖는 dictionary 새로 생성
# API 요청 반복문 중 data 추출과 동시에 movie code를 key값으로 data를 dictionary로 저장하기 위해 영화명(국문)을 key값으로 movie code를 value로 갖는 dictionary를 만들어줌
```

```python
'''
시행착오 1
'''
with open('movie.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 영화코드를 리스트로 생성
    for row in reader:
        mov_Nm_list.append(row['영화명(국문)'])
        mov_Cd_dict[row['영화명(국문)']] = row['영화 대표코드']


for mov_Nm in mov_Nm_list: # movie.csv에서 추출한 영화명(국문)을 query에 넣어주어 요청 보냄
    need_data = {}
    query = mov_Nm
    API_URL = f'{BASE_URL}?query={query}'
    # 요청 보내기
    response = requests.get(API_URL, headers=HEADERS).json() # 파이썬이 접근 가능한 dictionary 형태로 data를 받음
    items = response.get('items')
    need_data['네이버 영화 정보'] = items[0].get('link')
    need_data['영화 썸네일 이미지'] = items[0].get('image')
    need_data['네티즌 평점'] = items[0].get('userRating')
    mov_data[mov_Nm] = need_data
    time.sleep(0.01)
```

#### 오류 발견1

```python
# 위 코드는 'TypeError: 'NoneType' object is not subscriptable'와 같은 에러 발생
# 전체 data를 추출하는 아래의 코드를 통해 오류 원인 파악

for mov_Nm in mov_Nm_list: # movie.csv에서 추출한 영화명(국문)을 query에 넣어주어 요청 보냄
    need_data = {}
    query = mov_Nm
    API_URL = f'{BASE_URL}?query={query}'
    # 요청 보내기
    response = requests.get(API_URL, headers=HEADERS).json() # 파이썬이 접근 가능한 dictionary 형태로 data를 받음
    mov_data[mov_Nm] = response
    time.sleep(0.01)

# 파악 결과 너무 빠른 요청 속도로 영화 data가 정확히 추출이 안되는 경우 발생
# 아래의 코드를 추가하여 문제 해결
import time
time.sleep(0.1)

# '영화명(국문)'의 중복으로 원하는 data가 추출되지 않는 문제 발견
# '감독'으로 '영화면(국문)'이 중복되는 영화 중 원하는 영화 추출
```

#### 오류 발견2

```python
'''
시행착오2
'''
with open('movie.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 영화코드를 리스트로 생성
    for row in reader:
        mov_Nm_list.append(row['영화명(국문)'])
        mov_Cd_dict[row['영화명(국문)']] = row['영화 대표코드']
        mov_dir[row['영화명(국문)']] = (row['감독'] + '|')
        mov_dir2[row['영화명(국문)']] = (row['감독'])
        
for mov_Nm in mov_Nm_list: # movie.csv에서 추출한 영화명(국문)을 query에 넣어주어 요청 보냄
    need_data = {}
    query = mov_Nm
    API_URL = f'{BASE_URL}?query={query}'
    # 요청 보내기
    response = requests.get(API_URL, headers=HEADERS).json() # 파이썬이 접근 가능한 dictionary 형태로 data를 받음
    items = response.get('items')
    for i in range(len(items)):
        if items[i].get('director') == mov_dir[mov_Nm] or items[i].get('director') == mov_dir2[mov_Nm]: # 감독명을 통해 원하는 영화만 추출
            need_data['네이버 영화 정보'] = items[i].get('link')
            need_data['영화 썸네일 이미지'] = items[i].get('image')
            need_data['네티즌 평점'] = items[i].get('userRating')
    mov_data[mov_Cd_dict[mov_Nm]] = need_data

    time.sleep(0.1)
    
# 감독명 한국어 표기 차이로 인해 조건문을 통과하지 못하는 data가 발생
```

```python
'''
시행착오3
'''
with open('movie.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 영화코드를 리스트로 생성
    for row in reader:
        mov_Nm_list.append(row['영화명(국문)'])
        mov_Cd_dict[row['영화명(국문)']] = row['영화 대표코드']
        mov_dir[row['영화명(국문)']] = (row['감독'] + '|')
        mov_dir2[row['영화명(국문)']] = (row['감독'])
        mov_open[row['영화명(국문)']] = row['개봉연도'][0:4]
        
for mov_Nm in mov_Nm_list: # movie.csv에서 추출한 영화명(국문)을 query에 넣어주어 요청 보냄
    need_data = {}
    query = mov_Nm
    API_URL = f'{BASE_URL}?query={query}'
    # 요청 보내기
    response = requests.get(API_URL, headers=HEADERS).json() # 파이썬이 접근 가능한 dictionary 형태로 data를 받음
    items = response.get('items')
    for i in range(len(items)):
        if items[i].get('director') == mov_dir[mov_Nm] or items[i].get('director') == mov_dir2[mov_Nm] or items[i].get('title') == 'BIFAN2019 판타스틱 단편 걸작선 1':
            need_data['네이버 영화 정보'] = items[i].get('link')
            need_data['영화 썸네일 이미지'] = items[i].get('image')
            need_data['네티즌 평점'] = items[i].get('userRating')
        else:
            if items[i].get('pubDate') == mov_open[mov_Nm]:
                need_data['네이버 영화 정보'] = items[i].get('link')
                need_data['영화 썸네일 이미지'] = items[i].get('image')
                need_data['네티즌 평점'] = items[i].get('userRating')

    mov_data[mov_Cd_dict[mov_Nm]] = need_data

    time.sleep(0.1)
    
# value가 나오지 않는 data가 8개까지 감소
```

#### 오류 해결 및 최종

```python
'''
최종 data 추출 코드
'''
# 시행착오
# 네이버와 영진위의 개봉일 기준이 달라 원하는 data가 아닌 다른 data가 들어감을 확인, 개봉일 탐색은 폐기
# 응답 data 중 'display' == 1 이라면 중복이 되지 않았다는 것을 의미, 가장 먼저 'display' == 1임을 확인
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
```



#### 'movie_naver.csv'에 data 쓰기

```python
with open('movie_naver.csv', 'w', newline = '',  encoding = 'utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('네이버 영화 정보 URL', '영화 썸네일 이미지', '네티즌 평점', )
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    # 필드 이름을 csv파일 최상단에 작성한다.
    writer.writeheader()

    #Dictionary를 순회하며 key 값에 맞는 value 를 한줄씩 작성한다.
    for data in mov_data.values():
        writer.writerow(data)
```







## 문제2

### 프로젝트 목적 설정

향후 영화 목록에서 포스터 이미지로 사용할 이미지 파일을 앞서 네이버 영화 검색 API를 통해 얻은 이미지 URL에서 추출해서 저장한다.

- ##### 요청

  - 영화 썸네일 이미지의 URL

- ##### 응답

  - 응답 받은 결과를 파일로 저장합니다. 반드시 wb 옵션으로 저장
  - 저장되는 파일명은 images 폴더 내에 영진위 영화 대표코드.jpg

```python
import requests

thumb_URL = 'https://ssl.pstatic.net/imgmovie/mdi/mit110/1590/159070_P13_114738.jpg'

with open('images/test.jpg', 'wb') as f: # wb => write binary
    response = requests.get(thumb_URL) # URL 요청
    f.write(response.content) # 내용을 저장
```



#### 코드 구성 구상 및  구현

```python
# 'movie_naver.csv'에서 '영화 썸네일 이미지' 항목의 data를 모두 읽어옴
# 반복문을 통해 위의 코드 중 thumb_URL에 data를 대입하여 이미지 파일 추출
# 이미지 파일의 이름을 설정하기 위해 '영화코드' data 추출
```

#### 최종 코드

```python
import requests
import csv

image_URL = []
mov_Cd = {}

with open('movie_naver.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 URL을 리스트에 저장
    for row in reader:
        image_URL.append(row['영화 썸네일 이미지'])
        mov_Cd[row['영화 썸네일 이미지']] = row['영화코드']

for URL in image_URL:
    file_name = mov_Cd[URL]
    if len(URL) > 1:
        with open(f'images/{file_name}.jpg', 'wb') as f: # wb => write binary
            response = requests.get(URL) 
            f.write(response.content) # 내용을 저장
```

