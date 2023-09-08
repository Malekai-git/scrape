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
    
    pattern = r"(\$\s*\d{1,3}(?:[,\s]\d{3})*)\s*-\s*(\$\s*\d{1,3}(?:[,\s]\d{3})*)?\s*(\/\s*\w+)?"
    matches = re.findall(pattern, text)
    salary_data = []

    for match in matches:
        min_salary = match[0].replace('$', '').replace(',', '').strip() if match[0] else 'Unknown'
        max_salary = match[1].replace('$', '').replace(',', '').strip() if match[1] else 'Unknown'
        period = match[2].replace('/', '').strip() if len(match) > 2 and match[2] else 'Unknown'

        salary_data.append({
            "min_salary": min_salary,
            "max_salary": max_salary,
            "period": period,
        })
    
    return jsonify({"salaries": salary_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
