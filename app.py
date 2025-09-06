import streamlit as st
import feedparser
from langdetect import detect
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 언어별 라이브러리
from konlpy.tag import Okt
import jieba
from janome.tokenizer import Tokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
nltk.download("stopwords")

# 한국어/일본어 객체
okt = Okt()
janome_tagger = Tokenizer()

# ✅ 불용어 사전
stopwords_ko = {"것","수","등","들","및","에서","하다","까지","부터","그리고","그러나","때문","이것","저것","그것"}
stopwords_ja = {"こと","これ","それ","ため","よう","もの","さん","して","いる","ある","なる","また","そして","しかし"}
stopwords_zh = {"的","了","在","是","我","有","和","就","不","人","都","一个","上","也","很","到","说","要","去","你"}
stopwords_en = set(stopwords.words("english")) | {"said","one","like","also","would","could","us","many","new","people"}

def build_query(include_terms=None, exclude_terms=None, mode="AND"):
    query_parts = []
    if include_terms:
        if mode.upper() == "AND":
            query_parts.append(" ".join(include_terms))
        elif mode.upper() == "OR":
            query_parts.append("(" + " OR ".join(include_terms) + ")")
    if exclude_terms:
        query_parts.append(" ".join(f"-{term.strip()}" for term in exclude_terms))
    return " ".join(query_parts)


def get_text_before_dash(text: str) -> str:
    if "-" in text:
        return text.split("-")[0]
    return text

# 뉴스 가져오기
def fetch_news(query, site=None, lang="en", region="US"):
    from urllib.parse import quote
    query = quote(query)
    print(f"▶ Fetching news for query: {query}, lang: {lang}, region: {region}")
    if site:
        query = f"{query} site:{site}"
    url = f"https://news.google.com/rss/search?q={query}&hl={lang}&gl={region}&ceid={region}:{lang}"
    feed = feedparser.parse(url)
    #return [entry.title + " " + entry.description for entry in feed.entries]
    return [get_text_before_dash(entry.title) for entry in feed.entries]

# 토크나이즈
def tokenize_and_clean(text, lang):
    tokens = []
    if lang == "ko":
        tokens = [w for w, pos in okt.pos(text) if pos in ["Noun", "Adjective"]]
        tokens = [w for w in tokens if w not in stopwords_ko]
    elif lang == "ja":
        tokens = [t.surface for t in janome_tagger.tokenize(text) 
                  if t.part_of_speech.startswith("名詞") or t.part_of_speech.startswith("形容詞")]
        tokens = [w for w in tokens if w not in stopwords_ja]
    elif lang == "zh":
        tokens = [w for w in jieba.cut(text) if w not in stopwords_zh and len(w) > 1]
    else:  # 영어 기본
        tokens = [w for w in word_tokenize(text) if w.isalpha() and w.lower() not in stopwords_en]
    return [w.lower().strip() for w in tokens if w.strip()]

# 파이프라인 실행
def run_pipeline(query, site=None, lang="en", region="US"):
    docs = fetch_news(query, site, lang, region)
    all_tokens = []
    for doc in docs:
        try:
            detected_lang = detect(doc)
        except:
            detected_lang = "en"
        all_tokens.extend(tokenize_and_clean(doc, detected_lang))
    return Counter(all_tokens), len(docs)

# ===============================
# Streamlit 웹 인터페이스
# ===============================
st.title("🌏 다국어 뉴스 워드클라우드")

query1 = st.text_input("검색어를 콤마로 분리해서 입력하세요", "김주애").split(",")
query2 = st.text_input("검색 배제 단어를 콤마로 분리해서 입력하세요", "").split(",")

query = build_query(include_terms=query1, exclude_terms=query2, mode="AND")
print(f"▶ 최종 검색어: {query}")

col1, col2 = st.columns([1, 1])  

with col1:
    lang = st.selectbox("언어", ["한국어", "일본어", "중국어", "영어"])
    lang_option = {"한국어":"ko", "일본어":"ja", "중국어":"zh-CN", "영어":"en"}[lang]
with col2:
    region = st.selectbox("지역", ["한국", "일본", "중국", "미국"])
    region_option = {"한국":"KR", "일본":"JP", "중국":"CN", "미국":"US"}[region]

if st.button("워드 클라우드 생성 Submit Here ▶ "):
    freq, len_docs = run_pipeline(query, lang=lang_option, region=region_option)
    if not freq:
        st.warning("⚠️ 뉴스에서 단어를 찾지 못했습니다. 다른 검색어를 입력하세요.")
    else:
        # ✅ 운영체제에 맞는 폰트 경로 지정 (윈도우 기본값)
        font_path = "C:/Windows/Fonts/malgun.ttf"

        wc = WordCloud(
            font_path=font_path,
            width=800, height=600, background_color="white"
        ).generate_from_frequencies(freq)

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
        st.success(f"✅ {len_docs}개의 뉴스에서 단어를 추출했습니다.")