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
    