import streamlit as st
import requests
import re
from bs4 import BeautifulSoup

st.set_page_config(page_title="YT Post Downloader", page_icon="📸")

st.title("📸 YouTube Post Image Grabber")
st.write("コミュニティ投稿のURLを貼ると、画像を抽出します。")

url = st.text_input("URLをペースト:", placeholder="https://www.youtube.com/post/...")

if url:
    with st.spinner('画像を探しています...'):
        try:
            # 1. ページのHTMLを取得
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            response = requests.get(url, headers=headers)
            html = response.text

            # 2. og:imageタグからURLを取得（一番簡単な方法）
            soup = BeautifulSoup(html, 'html.parser')
            meta_img = soup.find("meta", property="og:image")
            
            if meta_img:
                img_url = meta_img["content"]
                
                # YouTubeのog:imageは低画質な場合があるため、サイズ指定があれば除去
                # (例: =s640 を消すとフルサイズになることが多い)
                high_res_url = re.sub(r'=s\d+.*', '', img_url)

                # 3. 画面に表示
                st.image(high_res_url, caption="抽出された画像", use_container_width=True)

                # 4. ダウンロードボタン（バイナリで取得）
                img_data = requests.get(high_res_url).content
                st.download_button(
                    label="高画質画像を保存",
                    data=img_data,
                    file_name="yt_post_image.jpg",
                    mime="image/jpeg"
                )
            else:
                st.error("画像が見つかりませんでした。URLが正しいか確認してください。")
        
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()
st.caption("※YouTubeの仕様変更により動かなくなる場合があります。")
