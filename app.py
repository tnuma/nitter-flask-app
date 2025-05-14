from flask import Flask, Response
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def home():
    return "Nitter API is running."

@app.route("/nitter-feed")
def nitter_feed():
    nitter_url = "https://nitter.net/Nanshindo_top"  # ← your_account を自社アカウントに変更
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(nitter_url, headers=headers)
    if response.status_code != 200:
        return Response("Failed to fetch Nitter feed", status=500)

    soup = BeautifulSoup(response.text, "html.parser")
    tweets = soup.find_all("div", class_="timeline-item")
    html = ""
    for tweet in tweets[:5]:
        content = tweet.find("div", class_="tweet-content")
        link = tweet.find("a", class_="tweet-link")['href']
        html += f'<div class="tweet">{content}<br><a href="https://nitter.net{link}" target="_blank">続きを読む</a></div>\n'

    return html


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが指定するポートを取得
    app.run(host="0.0.0.0", port=port)
