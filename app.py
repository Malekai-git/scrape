from flask import Flask, request, jsonify
import requests
import re
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/scrape_salary', methods=['POST'])
def scrape_salary():
    try:
        logging.info("Received a request.")
        url = request.json['url']
        logging.info(f"URL to be scraped: {url}")
        response = requests.get(url)
        
        if response.status_code != 200:
            logging.warning("Failed to fetch the URL.")
            return jsonify({"error": "Failed to fetch URL"}), 400
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        pattern = r"(\W|^)(?P<currency>\$)?\s*(?P<min>\d{1,3}(?:[,\s]\d{3})*)(?:\s*-\s*(?P<max>\d{1,3}(?:[,\s]\d{3})*))?\s*(?P<period>\/\s*\w+)?"
        
        salaries = re.findall(pattern, text)
        extracted_salaries = []
        for salary_match in salaries:
            currency = salary_match[2] if salary_match[2] else 'Unknown'
            min_salary = salary_match[3] if salary_match[3] else 'Unknown'
            max_salary = salary_match[4] if salary_match[4] else 'Unknown'
            period = salary_match[5].replace('/', '').strip() if salary_match[5] else 'Unknown'
            
            extracted_salaries.append({
                'currency': currency,
                'min_salary': min_salary,
                'max_salary': max_salary,
                'period': period
            })

        return jsonify({"salaries": extracted_salaries})

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(port=5000)
