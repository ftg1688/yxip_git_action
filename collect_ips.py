import requests
from bs4 import BeautifulSoup
import re
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Retry logic for requests
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Target URL list
urls = ['https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
        'https://ip.164746.xyz']

# Regex to match IP addresses
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# Remove existing ip.txt if it exists
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# Create a file to store IP addresses
with open('ip.txt', 'w') as file:
    for url in urls:
        try:
            # Make HTTP request
            response = session.get(url, verify=False)  # Use `verify=False` if SSL issues persist
            soup = BeautifulSoup(response.text, 'html.parser')

            # Parse content for IPs
            if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
                elements = soup.find_all('tr')
            elif url == 'https://ip.164746.xyz':
                elements = soup.find_all('tr')
            else:
                elements = soup.find_all('li')

            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)

                for ip in ip_matches:
                    file.write(ip + '\n')
        except Exception as e:
            print(f"Error processing {url}: {e}")

print('IP addresses have been saved to ip.txt.')
