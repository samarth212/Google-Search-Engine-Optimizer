from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keywords = request.form['keywords']
        search_results = google_search(keywords)
        filtered_urls = filter_urls(search_results, keywords)
        return render_template('index.html', urls=filtered_urls)
    else:
        return render_template('index.html', urls=[])

def google_search(keywords):
    url = f"https://www.google.com/search?q={keywords}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    return response.text

def filter_urls(content, keywords):
    soup = BeautifulSoup(content, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('http') and any(keyword in link.text for keyword in keywords):
            urls.append(url)
    return urls

if __name__ == '__main__':
    app.run(debug=True)
