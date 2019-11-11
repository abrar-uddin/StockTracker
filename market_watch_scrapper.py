from bs4 import BeautifulSoup as bs
import requests
import xlsxwriter

url = 'https://www.marketwatch.com/investing/stock/tcehy'
response = requests.get(url, timeout=5)
content = bs(response.content, 'html.parser')

name = content.find('h1', {'class': 'company__name'}).contents[0]

# <meta content="41.79" name="price"/>
current_price = content.find('meta', {'name': 'price'}).get('content')

# #['34.54 - 50.43']
high_low = content.find_all('span', {'class': 'kv__value kv__primary'})[2].contents[0]

articles = []

for i in range(5):
    articles.append([
        # Title
        content.findAll("h3", {"class": "article__headline"})[i].find('a').text.strip(),
        # Link
        content.findAll("h3", {"class": "article__headline"})[i].find('a').get('href')
    ])

file = xlsxwriter.Workbook('Data.xlsx')
data = file.add_worksheet()

row = 0
col = 0

data.write(row, col, name)
data.write(row, col + 1, current_price)
data.write(row, col + 2, url)
data.write(row + 1, col, "52 Week Range")
data.write(row + 1, col + 1, high_low)

row = 4
for i in range(len(articles)):
    data.write(row + i, col, articles[i][0])
    data.write(row + i, col + 1, articles[i][1])

file.close()
