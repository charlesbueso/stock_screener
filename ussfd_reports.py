import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# url = "https://efdsearch.senate.gov/search/"
url = "https://efdsearch.senate.gov/search/view/annual/e6c2dc43-a04c-4b41-80f3-6fb6bf3902e5/"

#If there is no such folder, the script will create one automatically
folder_location = r'C:\\repos\\watchout\\reports'

response = requests.get(url)
soup= BeautifulSoup(response.text, "html.parser")     
print(soup)

# for link in soup.select("a[href$='.pdf']"):
#     #Name the pdf files using the last portion of each link which are unique in this case
#     filename = os.path.join(folder_location,link['href'].split('/')[-1])
#     with open(filename, 'wb') as f:
#         f.write(requests.get(urljoin(url,link['href'])).content)