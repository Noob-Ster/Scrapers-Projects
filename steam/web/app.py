from flask import Flask, render_template
import requests
import json

app = Flask(__name__)


@app.route('/steam/top_sellers')
def index():
    response = requests.get(
        url='http://127.0.0.1:1001/crawl.json?start_requests=true&spider_name=top_sellers').json()
    items = json.dumps(response.get('items'))
    return items


@app.route('/show')
def firstWebPage():
    users = ['john','ali','bilal']
    return render_template('index.html', user=users)


if __name__ == "__main__":
    app.run(debug=True)
