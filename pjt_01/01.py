import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

Boxoffice_List_50W = {}

for i in range(50, 0, -1):
    week_del = i

    targetDt = datetime(2019, 7, 13) - timedelta(weeks = week_del) #해당일로 부터 2주를 빼겠다.
    targetDt = targetDt.strftime('%Y%m%d')
    
    key = config('API_KEY')
    
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    api_url = f'{base_url}?key={key}&targetDt={targetDt}'

    response = requests.get(api_url)
    data = response.json()
    
    for rank in range(10):
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

