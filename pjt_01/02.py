import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

movieInfo_List = {}

code_List = []
with open('boxoffice.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        code_List.append(row['movieCode'])
        

for code in code_List:
    movieCd = code
    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?'
    api_url = f'{base_url}&key={key}&movieCd={movieCd}'

    response = requests.get(api_url)
    data = response.json()


    need_data = {}
    need_data['movieCd'] = data["movieInfoResult"]["movieInfo"]["movieCd"]
    need_data['movieNm'] = data["movieInfoResult"]["movieInfo"]["movieNm"]
    need_data['movieNmEn'] = data["movieInfoResult"]["movieInfo"]['movieNmEn']
    need_data['movieNmOg'] = data["movieInfoResult"]["movieInfo"]['movieNmOg']
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
