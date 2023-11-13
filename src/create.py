import requests
from bs4 import BeautifulSoup
import pdfkit

url = 'https://example.com'  # Replace with the URL you want to scrape
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Here you can process the soup object to customize what you scrape

    # Convert HTML to PDF
    pdfkit.from_string(str(soup), 'output.pdf')
else:
    print(f"Failed to retrieve the webpage: Status Code {response.status_code}")
