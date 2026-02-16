import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("YouTube Post Image Downloader")

# URL入力
url = st.text_input("YouTubeポストの共有URLを貼ってね")

if url:
    try:
        # ページのHTMLを取得
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # og:image (SNS共有用の画像URL) を探すのが一番手っ取り早い
        img_url = soup.find("meta", property="og:image")["content"]
        
        if img_url:
            st.image(img_url, caption="見つかった画像")
            # ダウンロードボタン
            st.download_button("画像を保存する", requests.get(img_url).content, "image.jpg")
    except Exception as e:
        st.error("うまく取得できなかったよ。URLが正しいか確認してね！")
