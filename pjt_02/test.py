import requests # 요청 보내는 모듈
from pprint import pprint
from decouple import config
import time
import csv

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

# 필수적인 요청변수
query = '그린치'
API_URL = f'{BASE_URL}?query={query}'
# 요청 보내기
response = requests.get(API_URL, headers=HEADERS).json() # 파이썬이 접근 가능한 dictionary 형태로 data를 받음

pprint(response)
