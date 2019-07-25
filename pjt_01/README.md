# PJT01

## 문제1

```python
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

Boxoffice_List_50W = {}

for i in range(50, 0, -1): # 같은 키값이라도 최신에 들어온 정보로 갱신되는 dictionary 성질을 이용하기 위하여 오래된 정보부터 받아와서 탐색
    week_del = i

    targetDt = datetime(2019, 7, 13) - timedelta(weeks = week_del) #해당일로부터 week_del주만큼 빼겠다.
    targetDt = targetDt.strftime('%Y%m%d') #20180725 같은 꼴로 만들기 위한 문법
    
    key = config('API_KEY') # 개인 키값을 숨김
    
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    api_url = f'{base_url}?key={key}&targetDt={targetDt}'
	# 한 주 전체 data를 받아야 했는데 주말 data만 받아옴....
    response = requests.get(api_url)
    data = response.json()
    
    for rank in range(10): # 랭킹을 매개로 반복문에 넣어주어 한주의 Top10 영화를 전부 탐색
        # 빈 dictionary인 need_data에 각 영화의 Value를 저장한다.
        # Boxoffice_List_50W에 영화제목을 Key값으로 하여 need_data의 Value들을 전달 받는다.
        # 영화제목을 Key값으로 받음으로써 중복되는 data들이 중복이 되거나 누락이 되지 않도록 만들었다.
        # 영화코드를 Key값으로 설정했다면 문제2를 푸는데 조금 더 이해하기 편했을 것으로 생각된다.
        need_data = {}
        need_data['movieName'] = data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieNm']
        need_data['movieCode'] = data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd']
        need_data['audiAcc'] = data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['audiAcc']
        Boxoffice_List_50W[data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieNm']] = need_data

with open('boxoffice.csv', 'w', newline = '',  encoding = 'utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('movieName', 'movieCode', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    # 필드 이름을 csv파일 최상단에 작성한다.
    writer.writeheader()

    #Dictionary를 순회하며 key 값에 맞는 value 를 한줄씩 작성한다.
    for Boxoffice_List in Boxoffice_List_50W.values():
        writer.writerow(Boxoffice_List)

```



## 문제2

```python
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

movieInfo_List = {}

code_List = []
# 문제1에서 생성한 boxoffice.csv 파일을 읽기
with open('boxoffice.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 영화코드를 리스트로 생성
    for row in reader:
        code_List.append(row['movieCode'])
        
# 앞서 생성한 코드 리스트를 돌면서 데이터를 받아옴
for code in code_List:
    movieCd = code
    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    api_url = f'{base_url}&key={key}&movieCd={movieCd}'

    response = requests.get(api_url)
    data = response.json()

	
    # 빈 dictionary인 need_data에 각 영화의 Value를 저장
    # 영화제목을 Key값으로 하여 movieInfo_List에 need_data 내부의 Value 전달
    need_data = {}
    need_data['movieCd'] = data["movieInfoResult"]["movieInfo"]["movieCd"]
    need_data['movieNm'] = data["movieInfoResult"]["movieInfo"]["movieNm"]
    need_data['movieNmEn'] = data["movieInfoResult"]["movieInfo"]['movieNmEn']
    need_data['movieNmOg'] = data["movieInfoResult"]["movieInfo"]['movieNmOg']
    # audits 항목과 director 항목의 data가 비어있는 영화가 있음을 발견하고
    # try, except 예외처리를 해서 건너뜀
    # if문을 통해서 예외처리가 가능할 수 있다고 생각됨
    try:
        need_data['watchGradeNm'] = data["movieInfoResult"]["movieInfo"]['audits'][0]['watchGradeNm']
    except:
        pass
    need_data['openDt'] = data["movieInfoResult"]["movieInfo"]['openDt']
    need_data['showTm'] = data["movieInfoResult"]["movieInfo"]['showTm']
    need_data['genres'] = data["movieInfoResult"]["movieInfo"]['genres']
    try:
        need_data['director'] = data["movieInfoResult"]["movieInfo"]['directors'][0]['peopleNm']
    except:
        pass
    movieInfo_List[data["movieInfoResult"]["movieInfo"]['movieNm']] = need_data

with open('movie.csv', 'w', newline = '',  encoding = 'utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'watchGradeNm', 'openDt', 'showTm', 'genres', 'director')
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    # 필드 이름을 csv파일 최상단에 작성한다.
    writer.writeheader()

    #Dictionary를 순회하며 key 값에 맞는 value 를 한줄씩 작성한다.
    for movieInfo in movieInfo_List.values():
        writer.writerow(movieInfo)

```



## 문제3

```python
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

# dirt_dict = {}
dirt_list = [] # 영화인 중 감독만 찾기 위한 반복문을 돌기 위한 영화인 리스트, 변수명 설정이 잘못됨
pCd_list = [] # 아무 역할이 없는 리스트, 제거 필요
dirt_Cd_list = [] # 감독 정보 추출 반복문을 돌기 위한 감독 코드 리스트
dirtInfo_List = {} # 감독 정보를 모아줄 감독 정보 dictionary

# 문제2에서 만든 movie.csv 읽기
with open('movie.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    # 읽은 데이터 중 'director' 항목의 데이터를 dirt_list에 모음, 영화인 이름이 저장됨
    for row in reader:
        dirt_list.append(row['director'])

for dirt in dirt_list: # 영화인명으로 영화인목록 리스트 추출
    peopleNm = dirt
    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
    api_url = f'{base_url}&key={key}&peopleNm={peopleNm}'

    response = requests.get(api_url)
    dirt_data = response.json()
	
    # 영화인목록에서 감독만 추출
    for dirt_d in dirt_data['peopleListResult']['peopleList']: 
        if dirt_d['repRoleNm'] == '감독': # 감독만 추출하는 조건문
            # dirt_dict[dirt_d['peopleCd']] = dirt_d # dirt_dict에 감독만 저장
            dirt_Cd_list.append(dirt_d['peopleCd']) # 감독 코드 리스트 생성


# 감독 코드를 통해 감독의 정보들을 수집
for pCd in dirt_Cd_list: 
    peopleCd = pCd
    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?'
    api_url = f'{base_url}&key={key}&peopleCd={peopleCd}'

    response = requests.get(api_url)
    data = response.json()

    # 빈 dictionary인 need_data에 각 감독의 Value를 저장
    # 감독이름을 Key값으로 하여 dirtInfo_List에 need_data 내부의 Value 전달
    need_data = {}
    
    # 데이터가 없는 항목들이 존재하여 try, except를 통해 데이터가 없는 항목을 건너뜀
    # 문제2와 동일하게 if문으로 처리가 가능할 것으로 보임
    try:
        need_data['directorCd'] = data["peopleInfoResult"]["peopleInfo"]["peopleCd"]
        need_data['directorNm'] = data["peopleInfoResult"]["peopleInfo"]["peopleNm"]
        need_data['repRoleNm'] = data["peopleInfoResult"]["peopleInfo"]["repRoleNm"]
        need_data['filmos'] = data["peopleInfoResult"]["peopleInfo"]["filmos"]

        dirtInfo_List[data["peopleInfoResult"]["peopleInfo"]['peopleNm']] = need_data
    except:
        pass

with open('director.csv', 'w', newline = '',  encoding = 'utf-8') as f:
    # 저장할 필드의 이름을 미리 지정한다.
    fieldnames = ('directorCd', 'directorNm', 'repRoleNm', 'filmos')
    writer = csv.DictWriter(f, fieldnames = fieldnames)

    # 필드 이름을 csv파일 최상단에 작성한다.
    writer.writeheader()

    #Dictionary를 순회하며 key 값에 맞는 value 를 한줄씩 작성한다.
    for irt_Info in dirtInfo_List.values():
        writer.writerow(dirt_Info)
```



### 문제점

```python
'''
1. 반복횟수가 너무 많아 시간이 오래걸리고 key 사용횟수를 빠르게 소진함. 반복문 단축 필요
2. try, except를 통해 데이터 손실 발생이 우려됨, if문과 같은 조금 더 안전한 방법 사용이 필요
3. 변수명의 적절한 설정 필요
4. 문제를 정확하게 파악하는 것 필요
'''
```



