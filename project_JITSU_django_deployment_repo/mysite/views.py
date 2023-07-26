from django.shortcuts import render
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Create your views here.
# 소프트웨어까지
base_url = "https://www.sophia-it.com/word-category/%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2"

# selenium set -------------------------------------------------------
# 웹 드라이버의 경로 지정 (다운로드한 웹 드라이버의 경로로 변경)
driver_path = 'C:\chromedriver'

# 웹 드라이버 옵션 설정 (headless 모드로 실행)
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# 웹 드라이버 생성
driver = webdriver.Chrome(options=options)


# 용어 카테고리 크롤링-------------------------------------------------
def crawling_category(url):
    response = requests.get(url)

    # 요청이 성공적으로 이루어졌는지 확인
    if response.status_code == 200:
        # HTML 문서를 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 클래스 이름을 사용하여 용어 목록 부분을 추출
        cat_list = soup.find('div', class_='wordCat')

        # 용어 목록이 있는지 확인
        if cat_list:
            # 각 용어와 뜻 추출하여 출력
            cats = cat_list.find_all('li')
            cat_all = []
            for cat in cats:
                cat_all.append(cat.find('a').text)
            return cat_all
        else:
            print("cat 목록을 찾을 수 없습니다.")

    else:
        print("사이트에 접속할 수 없습니다.")

    # 용어 크롤링---------------------------------------------------------


def crawling_word(url):
    response = requests.get(url)

    # 요청이 성공적으로 이루어졌는지 확인
    if response.status_code == 200:
        # HTML 문서를 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 클래스 이름을 사용하여 용어 목록 부분을 추출
        word_list = soup.find('div', class_='wordList')

        # 용어 목록이 있는지 확인
        if word_list:
            # 각 용어와 뜻 추출하여 출력
            words = word_list.find_all('li')
            word_all = []
            for word in words:
                word_all.append(word.string)
            return word_all
        else:
            print("word 목록을 찾을 수 없습니다.")

    else:
        print("사이트에 접속할 수 없습니다.")

    # 용어 정의 크롤링---------------------------------------------------


def crawling_meaning(word):
    url = f"https://www.sophia-it.com/content/{word}"
    response = requests.get(url)

    # 요청이 성공적으로 이루어졌는지 확인
    if response.status_code == 200:
        # HTML 문서를 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 클래스 이름을 사용하여 용어 목록 부분을 추출
        meaning = soup.find('td', class_='txts').p.text

        # 용어 목록이 있는지 확인
        if meaning:
            return (meaning)
        else:
            print("mean을 찾을 수 없습니다.")

    else:
        print("사이트에 접속할 수 없습니다.")

    # 일-한 번역 결과 크롤링-------------------------------------------------


def crawling_translate(jap):
    url = f"https://papago.naver.com/?sk=ja&tk=ko&hn=0&st={jap}"

    driver.get(url)

    # 번역 결과가 나타날 때까지 기다립니다. (명시적 대기)
    css_selector = "#txtTarget"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    # 번역 결과를 가져와 출력합니다.
    kor = driver.find_element(By.CSS_SELECTOR, css_selector).text
    driver.quit()

    return kor

# 1. 태그 저장-------------------------------------------------


# 용어사전/소프트웨어
url = "https://www.sophia-it.com/word-category/%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2"

# 소프트웨어 하위 전체 태그 목록
tag_all = crawling_category(url)

# 유저가 선택한 태그 목록
tag_list = ["OS"]
tag_dict = {}

# 2. 태그 하위 단어 통합-------------------------------------------------------

for tag in tag_list:
    url = "https://www.sophia-it.com/word-category/%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2/" + tag
    word1 = crawling_word(url)
    cats = crawling_category(url)
    for cat in cats:
        url = "https://www.sophia-it.com/word-category/%E3%82%BD%E3%83%95%E3%83%88%E3%82%A6%E3%82%A7%E3%82%A2/" + tag + "/" + cat
        word2 = crawling_word(url)
        word1 += word2
    tag_dict[tag] = word1  # 해당 태그 하위 전체 단어를 분류 없이 통합, 태그 : [단어목록]
#    print(tag_dict)


# 3. 단어 뜻 한국어로 번역(셀레니움)-----------------------------------------------

w = "オペレーティングシステム"  # 예시
print(crawling_translate(w))

# 4. 단어 정의 한국어로 번역(셀레니움)-----------------------------------------------------------------

m = crawling_meaning(w)
print(crawling_translate(m))

# (단어 뜻, 정의 번역 실행 예시 및 실행 시간 측정) ---------------------------------

w = "オペレーティングシステム"
m = crawling_meaning(w)
start_time = time.time()
print(w)
print(crawling_translate(w))
print(crawling_translate(m))
end_time = time.time()
execution_time = end_time - start_time
print(f"실행 시간: {execution_time:.6f}초")



