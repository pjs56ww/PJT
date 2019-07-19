import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

targetDt = datetime(2019, 7, 13) - timedelta(weeks = 1) #해당일로 부터 2주를 빼겠다.
targetDt = targetDt.strftime('%Y%m%d')

key = config('API_KEY')
base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
api_url = f'{base_url}?key={key}&targetDt={targetDt}'

response = requests.get(api_url)
data = response.json()

pprint(data)
