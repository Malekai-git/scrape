import requests

response = requests.post('http://127.0.0.1:5000/scrape_salary', json={"url": "https://recruiting.paylocity.com/recruiting/jobs/Details/520796/Urban-Dove-Charter-School/Sports-Based-Youth-Development-Coach"})
print(response.json())
