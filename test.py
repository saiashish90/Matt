import requests
from bs4 import BeautifulSoup

url = 'https://www.youtube.com/playlist?list=PLO7-VO1D0_6N2ePPlPE9NKCgUBA15aOk2'

data = requests.get(url)
data = data.text
soup = BeautifulSoup(data, features="html.parser")

h4 = soup.find_all("h4")
for h in h4:
    print(h.text)
