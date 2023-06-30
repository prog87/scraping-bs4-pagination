import requests
import os
from bs4 import BeautifulSoup
import lxml


#####################################################
# Pagination
#####################################################

# How To Get The HTML
root = 'https://subslikescript.com'  # this is the homepage of the website
website = f'{root}/movies_letter-A'  # concatenating the homepage with the movies section
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
# print(soup.prettify())  # prints the HTML of the website

# Pagination
pagination = soup.find('ul', class_='pagination')
pages = pagination.find_all('li', class_='page-item')
last_page = pages[-2].text

# Store each link in "links" list (href doesn't consider root aka "homepage", so we have to concatenate it later)

for page in range(1, int(last_page)+1)[:2]:
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='main-article')

    links = []
    for link in box.find_all('a', href=True):  # find_all returns a list
        links.append(link['href'])
    # Loop through the "links" list and sending a request to each link
    for link in links:
        result = requests.get(f'{root}/{link}')
        content = result.text
        soup = BeautifulSoup(content, 'lxml')

        for e in soup.select('article', class_='main-article'):
            name = e.h1.get_text(strip=True)
            html = e.find('div', class_='full-script').get_text(strip=True, separator=' ')
            try:
                os.mkdir('temp')
            except FileExistsError:
                    pass
            try:
                with open(f'temp/{name}.txt', 'w', encoding='utf-8') as file:
                    file.write(html)
                    file.close()
            except Exception as e:
                print(e)


