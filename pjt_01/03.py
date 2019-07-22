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

for dirt in dirt_list: # 감독명으로 영화인목록 리스트 추출
    peopleNm = dirt
    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?'
    api_url = f'{base_url}&key={key}&peopleNm={peopleNm}'

    response = requests.get(api_url)
    dirt_data = response.json()

    for dirt_d in dirt_data['peopleListResult']['peopleList']: # 영화인목록에서 감독만 추출
        if dirt_d['repRoleNm'] == '감독':
            # dirt_dict[dirt_d['peopleCd']] = dirt_d # dirt_dict에 감독만 저장
            dirt_Cd_list.append(dirt_d['peopleCd']) # 감독 코드 리스트 생성



for pCd in dirt_Cd_list:
    peopleCd = pCd
    key = config('API_KEY')
    base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?'
    api_url = f'{base_url}&key={key}&peopleCd={peopleCd}'

    response = requests.get(api_url)
    data = response.json()

    need_data = {}
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
    for dirt_Info in dirtInfo_List.values():
        writer.writerow(dirt_Info)