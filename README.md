# CrawlingServer

- 직업 사이트 **Incruit** 의 올라온 **"인터넷, IT, 통신, 모바일, 게임 업종"** 의 채용 정보를 일정한 시간마다 크롤링
- 스케쥴링을 하여 하루에 지정한 만큼 크롤링 실행

## 개발환경
- flask
- python3.6.8
- Beautifulsoup4
- MariaDB 10.3(?)

## 기능
1. 해당 크롤링한 **채용 공고 정보**를  
"공고 URL","공고 제목", "회사명", "회사 설립일", "기업 규모(대/중/소)","업종", "회사 주소","모집직종", "모집인원", "경력구분", "학력", "고용형태(정규직/인턴/계약직)", "근무지역", "급여", "직급", "모집 시작일", "모집 마감일", "필요서류"  
의 형태로 **엑셀파일로 저장**

2. 해당 크롤링한 **채용 공고 정보**를 **DB Server에 저장**

## 실행 순서
1. 채용 회사 정보 DB 저장
```bash
python company.py
```

2. 크롤링 서버 실행 => crawling.py를 실행해주는 flask 서버 실행
```bash
python init.py
```

