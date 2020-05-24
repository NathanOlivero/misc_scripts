

import requests
import os

def parse_url(url, headers, proxies):
    try:
        response = requests.get(url, headers=headers, proxies=proxies, stream=True)
        response.raise_for_status()
    except requests.HTTPError as exception:
        print(exception)
    except requests.exceptions.MissingSchema as exception:
        print(exception)

    peername = response.raw._connection.sock.socket.getpeername()
    socketname = response.raw._connection.sock.socket.getsockname()
    print("Socketname IP Address: " + str(socketname[0]) + " Port: " + str(socketname[1]))
    print("Peername IP Address: " + str(peername[0]) + " Port: " + str(peername[1]))
    print(response.headers)
    response.close()

url = "https://nathanolivero.com/"

proxies = {
    "http": "http://12.226.155.29:3128",
#    "https": "https://69.88.123.106:8080"
}
headers = {
 'user-agent': "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
}

parse_url(url, headers, proxies)
