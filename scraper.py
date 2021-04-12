import requests
from bs4 import BeautifulSoup
import string
import os


current_link = "https://www.nature.com/nature/articles"


def category_selector(user_category, cur_link):

    r = requests.get(cur_link)
    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.find_all("article")

    target_links = dict()
    for article in articles:
        category = article.find("span", {'class': 'c-meta__type'}).text.strip()
        if category == user_category:
            find_title = article.find("a")
            title = find_title.text.strip()
            find_link = find_title.get("href")
            link = "https://www.nature.com" + find_link
            target_links[title] = link
    return target_links


def fix_filenames(name):
    remove_punctuation = name.translate(name.maketrans(" ", "_", string.punctuation))
    return remove_punctuation


def extract_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    body = soup.find("div", {"class":"article-item__body"})
    if body is None:
        bodys = soup.findAll('div', {'class': 'Theme-Layer-BodyText--inner'})
        full_text = ''
        for body in bodys:
            text = body.find('p').text.strip()
            full_text += text + '\n'
    else:
        full_text = body.text.strip()
    return full_text


def save_to_file(name, content):
    with open(f"{name}.txt", "w", encoding="UTF-8") as file:
        file.write(content)


def user_input():
    number_of_pages = int(input())
    category = str(input())
    return number_of_pages, category


def new_page_link(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    next_page = soup.find('li', {'data-page': 'next'})
    next_page_href = next_page.find('a').get('href')
    return "https://www.nature.com"+next_page_href


def on_page_operation(target_links):
    for k, v in target_links.items():
        article_name = fix_filenames(k)
        contents = extract_text(v)
        save_to_file(article_name, contents)


n_pages, category = user_input()
cwd = str(os.getcwd())
for i in range(1, n_pages+1):
    os.mkdir(cwd+f'\\Page_{i}')
    os.chdir(cwd+f'\\Page_{i}')
    target_links = category_selector(category, current_link)
    on_page_operation(target_links)
    current_link = new_page_link(current_link)
    os.chdir(cwd)

