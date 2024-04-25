from flask import Flask, render_template, request
from googleapiclient.discovery import build

API_KEY = 'AIzaSyBFK7YUOZ0ZSHKmOiVsy638y4RkrsGSIRs'

SEARCH_ENGINE_ID = '62e3fbd85dd204709'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            keywords = request.form['keywords']
            service = build("customsearch", "v1", developerKey=API_KEY)
            
            search_params = {
                "cx": SEARCH_ENGINE_ID,
                "q": keywords,
            }
            
            search_results = service.cse().list(**search_params).execute()
            
            urls = [item['link'] for item in search_results.get('items', [])]
            return render_template('index.html', urls=urls, search_terms=keywords)
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return render_template('index.html', urls=[], search_terms="")

