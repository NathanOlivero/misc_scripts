import requests
from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup
import os

class HTMLTableParser:
    def parse_url(self, url, proxies):
        try:
            response = requests.get(url, proxies=proxies)
            response.raise_for_status()
        except requests.HTTPError as exception:
            print(exception)
        except requests.exceptions.MissingSchema as exception:
            print(exception)

        soup = BeautifulSoup(response.text, 'lxml')
        tableList = soup.find_all('table')
        for table in tableList:
            for row in table.find_all('tr'):
                for td_tag in row.find_all('td', class_="useragent"):
                    print(type(td_tag.get_text()))
                    print(td_tag)
                    # with open("user-agent-headers.txt", "w", newline='\r\n') as f:
                    #     f.write(td_tag.get_text())
                    # f.close()
#url = "https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/"
url = "https://nathanolivero.com/"
proxies = {
#    "http": "http://205.201.49.141:53281",
    "https": "104.129.41.21:31282"
}
headers = {
 'user-agent': "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
}

tableParser = HTMLTableParser()
tableParser.parse_url(url, proxies)


import requests
from requests.auth import HTTPProxyAuth

proxy_string = 'http://user:password@url_proxt:port_proxy'

s = requests.Session()
s.proxies = {"http": proxy_string , "https": proxy_string}
s.auth = HTTPProxyAuth(user,password)

r = s.get('http://www.google.com') # OK
print(r.text)
r = s.get('https://www.google.com',proxies={"http": proxy_string , "https": proxy_string}) #OK
print(r.text)
r = s.get('https://www.google.com') # KO
print(r.text)
