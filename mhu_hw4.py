import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

# from flask import Flask, render_template, jsonify, request
# app = Flask(__name__)



headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')
# select를 이용해서, tr들을 불러오기
musics = soup.select('#body-content > div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr')

# song은 tbody아래의 모든 tr의 리스트이고, 그 중에 하나를 골라서 for 반복을 돌린다.
for song in musics:
    rank = song.select_one('td.number').text
    print(rank)
    # song 안에 a 가 있으면,
    a_tag1 = song.select_one('td.info > a.title.ellipsis')
    a_tag2 = song.select_one('td.info > a.artist.ellipsis')
    if a_tag1 is not None: #이게 왜 필요한 지 모르겠다. 없으면 에러남.
        title = a_tag1.text
        print(title)
    if a_tag2 is not None:
        singer = a_tag2.text
        print(singer)
        # Doc만들어 mongo DB에 insert 하기
        Doc = {
            'rank': rank,
            'title': title,
            'singer': singer
        }
        db.musicChart.insert_one(Doc)
