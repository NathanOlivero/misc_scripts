import webbrowser, sys, requests, bs4

# url = "https://www.bbc.com/news"
# res = requests.get(url)
# try:
#     res.raise_for_status()
# except Exception as exc:
#     print('There was a problem: %s' % (exc))
#
# with open('D:\\olive\\Documents\\Code\\Upwork\\example.html', 'wb') as f:
#     f.write(res.content)
#     f.close()

with open('D:\\olive\\Documents\\Code\\Upwork\\example.html', 'r') as f:
    exampleFile = f.read()
    f.close()


soup = bs4.BeautifulSoup(exampleFile, 'html.parser')
elems = soup.select('#news-top-stories-container')

print(type(elems))
print(len(elems))
print(type(elems[0]))
print(str(elems[0])) # The Tag object as a string.
print(elems[0].getText())
print(elems[0].attrs)
