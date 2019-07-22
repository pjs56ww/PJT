import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

# dirt_dict = {}
dirt_list = []
pCd_list = []
dirt_Cd_list = []
dirtInfo_List = {}


with open('movie.csv', 'r', newline = '',  encoding = 'utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        dirt_list.append(row['director'])
print(dirt_list)


peopleNm = dirt_list[0]

key = config('API_KEY')
base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
api_url = f'{base_url}&key={key}&peopleNm={peopleNm}'

response = requests.get(api_url)
dirt_data = response.json()

for dirt_d in dirt_data['peopleListResult']['peopleList']: # 영화인목록에서 감독만 추출
    if dirt_d['repRoleNm'] == '감독':
        # dirt_dict[dirt_d['peopleCd']] = dirt_d # dirt_dict에 감독만 저장
        dirt_Cd_list.append(dirt_d['peopleCd']) # 감독 코드 리스트 생성

print(dirt_Cd_list)