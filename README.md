# wordcloud-app
이 프로젝트는 구글 뉴스 RSS를 수집하고, 언어를 자동으로 감지하여   불용어(stopwords)를 제거한 후 **워드클라우드**를 생성하는 Streamlit 앱입니다.   한국어, 영어, 일본어, 중국어를 지원합니다.


## 📌 주요 기능
- 검색어 입력 시 Google News RSS에서 최신 뉴스 수집
- 언어 자동 감지 (ko, en, ja, zh)
- 언어별 토크나이즈 + 불용어 제거
- 워드클라우드 시각화 (자동 이미지 출력)
- Streamlit 웹 앱 형태로 동작

---

## ⚙️ 설치 방법

### 1. 저장소 클론
git clone https://github.com/thumos1/wordcloud-app.git
cd wordcloud-app

### 2. 가상환경 생성(권장)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

### 3. 필요 라이브러리 설치
pip install -r requirements.txt

### 4. 실행방법
streamlit run app.py

### 5. 프로젝트구조
wordcloud-app/
│── app.py                # Streamlit 앱 코드
│── requirements.txt      # 패키지 목록
└── README.md             # 프로젝트 설명
