from flask import Flask, request, jsonify
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape_salary', methods=['POST'])
def scrape_salary():
    url = request.json['url']
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch URL"}), 400
    
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    
    pattern = r"\$\s*\d{1,3}(?:[,\s]\d{3})*(?:\s*-\s*\$\s*\d{1,3}(?:[,\s]\d{3})*)?(?:\s*\/\s*\w+)?"
    salaries = re.findall(pattern, text)
    
    return jsonify({"salaries": salaries})

if __name__ == '__main__':
    app.run(port=5000)
