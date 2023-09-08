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
    
    # Updated regex pattern to capture currency and time period
    pattern = r"(\W|^)(?P<currency>\$)?\s*(?P<min>\d{1,3}(?:[,\s]\d{3})*)(?:\s*-\s*(?P<max>\d{1,3}(?:[,\s]\d{3})*))?\s*(?P<period>\/\s*\w+)?"
    
    salaries = re.findall(pattern, text)
    
    # Creating a list to hold the extracted data in dictionary form
    extracted_salaries = []
    for salary_match in salaries:
        currency = salary_match[1] if salary_match[1] else 'Unknown'  # Adjusted to correct index
        min_salary = salary_match[2].replace(',', '').replace(' ', '').strip() if salary_match[2] else 'Unknown'  # Cleaned up
        max_salary = salary_match[3].replace(',', '').replace(' ', '').strip() if salary_match[3] else 'Unknown'  # Cleaned up
        period = salary_match[4].replace('/', '').strip() if salary_match[4] else 'Unknown'
        
        extracted_salaries.append({
            'currency': currency,
            'min_salary': min_salary,
            'max_salary': max_salary,
            'period': period
        })

    return jsonify({"salaries": extracted_salaries})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
