#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
session = requests.Session()

session.headers['User-Agent']


baseurl = "https://notmeat.ru/#rec210908899"
url = "https://notmeat.ru/"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}


def createSoup(header: dict, url: str, session:requests.sessions.Session)->bs4.BeautifulSoup:
    response = session.get(baseurl, headers=headers)
    return BeautifulSoup(response.text, 'html.parser')

def buildTree(html_item: str, html_class: str) -> dict:
    container = html_soup.find_all([html_item], class_=lambda x: x == html_class)

    links = [line.get("href") for line in container]
    titles = [line.text for line in container]
    return dict(zip(titles, links))


def traverseTree(tree: dict, html_item: str, html_class: str) -> dict:
    traversal_dict = {}
    for i in tree:
        try:
            response = session.get(url[:-1] + tree[i], headers=headers)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            page = html_soup.find_all(html_item, 
                            class_=lambda x: x == html_class)
            traversal_dict[i] = page
        except:
            pass

def findItemsByContent(traversal_dict: dict, key_word: str) -> dict:
    data = {}
    for i in traversal_dict:
        if len(traversal_dict[i]) > 0:
            for j in traversal_dict[i]:
                if key_word in str(j):
                    data[i] = j


def dataCleanup(data: dict, rx: dict) -> dict: #{'<[^>]+>':'', 'Состав:'', '[(]': ', ', '[)]': ''}
    for i in data:
        for x in rx:
            data[i] = re.sub(x, rx[x], str(data[i]))
    return data

def simpleCrawler()-> dict:
    pass

def runSimpleCrawler() -> dict:
    data = simpleCrawler()
    for i in data: 
        data[i] = str(data[i])[:-1].strip()
        data[i] = set(data[i].split(", "))
    return data

def scrollingCrawler() -> dict:
    pass

baseurl = "https://shop.soyka.ru"
url = "https://shop.soyka.ru/catalog/rastitelnye-myasnye-alternativy/#"
# response = session.get(url, headers=headers)
# chromrdriver = "/home/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromrdriver
# driver = webdriver.Chrome(chromrdriver)
driver = webdriver.Firefox(executable_path="./drivers/geckodriver")
driver.get(url)

ScrollNumber = 10
for i in range(1,ScrollNumber):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

file = open('DS.html', 'w')
file.write(driver.page_source)
file.close()

driver.close()


file = open('DS.html', 'r')
page = file.read()
file.close()

html_soup = BeautifulSoup(page, 'html.parser')

container = html_soup.find_all(["a"], 
                               class_=lambda x: x == 'c-catalog__section__name')


print(len(container))
datadict = []
for i in container:
    print(i.text)
    print(i.get("href"))
    datadict.append({"Название": i.text.split(", ")[0], "Вес": i.text.split(", ")[1], "Ссылка": i.get("href")})


# In[157]:


datadict


# In[160]:


def cleanHTML(raw: str)-> str:
    CLEANR = re.compile('<.*?>') 
    return re.sub(CLEANR, '', raw)

for i in datadict:
#     print(url[:-1] + tree[i])
    try:
        response = session.get(baseurl + i["Ссылка"], headers=headers)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        current_price = html_soup.find_all("div", 
                           class_=lambda x: x == "c-product-price-value is-price-now")
        current_price = cleanHTML(str(current_price[0]))
            
        old_price = html_soup.find_all("div", 
                           class_=lambda x: x == "c-product-price-line-through-value")
        
        old_price = cleanHTML(str(old_price[0]))
            
        properties = html_soup.find_all("div", 
                           class_=lambda x: x == "c-product-property")
        for j in properties:
            j = cleanHTML(str(j))
        
        i["СтараяЦена"] = old_price
        i["Цена"] = current_price
        i["Описание"] = properties
    except:
        pass


# In[164]:


for i in datadict:
    temp = []
    for j in i["Описание"]:
        temp.append(cleanHTML(str(j)))
    i["Описание"] = temp


# In[181]:


for i in range(len(datadict)):
    temp = []
    try:
        datadict[i]["СтараяЦена"] = float(re.sub("[^0-9.]", "", datadict[i]["СтараяЦена"]))
    except ValueError:
        print(datadict[i]["СтараяЦена"])
    
    try:
        datadict[i]["Цена"] = float(re.sub("[^0-9.]", "", datadict[i]["Цена"]))
    except ValueError:
        print(datadict[i]["Цена"])
    for j in range(len(datadict[i]["Описание"])):
        temp.append(
            re.sub('(\\t\\t\\t\\t\\t)', ' ', datadict[i]["Описание"][j])
        )
        temp[-1] = re.sub('[\\n\\t]', '', temp[-1])
#         i["Описание"][j] = 
    datadict[i]["Описание"] = temp


# In[186]:


datadict


# In[188]:


for i in datadict:
    try:
        i["Состав"] = i['Описание'][0][8:-1]
        i["Изготовитель"] = i['Описание'][2].split(":")[1].strip()
        i["Марка"] = i['Описание'][3].split(":")[1].strip()
        i["СрокГодности"] = i['Описание'][4].split(":")[1].strip()
        i["ТемператураХранения"] = i['Описание'][5].split(":")[1].strip()
        i["ЭнергетическаяЦенность"] = i['Описание'][7].split(":")[1].strip()
        i["Белки"] = i['Описание'][8].split(":")[1].strip()
        i["Углеводы"] = i['Описание'][9].split(":")[1].strip()
        i["Жиры"] = i['Описание'][10].split(":")[1].strip()
    except IndexError:
        print(i)
        


# In[269]:


import pandas as pd

df = pd.DataFrame(datadict)


# In[ ]:


[^-*0-9.]


# In[270]:


df.Название = df.Название.str.replace( "«(.*?)»", "").str.strip()
df.ТемператураХранения = df.ТемператураХранения.str.replace("±(.*)", "").str.strip()
numeric = ["СрокГодности", "ТемператураХранения", "ЭнергетическаяЦенность"]
for col in numeric:
    df[col] = df[col].str.replace("[^-*0-9.]", "").str.strip()
df.Вес = df.Вес.str.replace("\[Россия\]", "").str.strip()
df.Вес = df.Вес.str.replace("\[\]", "").str.strip()
df.Вес = df.Вес.str.replace(",", ".").str.strip()
kg = df[df.Вес.str.contains('кг')].index
df.Вес = df.Вес.str.replace("[« ».a-zа-яА-Я]", "").str.strip()
numeric = ["Вес", "СрокГодности", "ТемператураХранения", "ЭнергетическаяЦенность"]
for i in numeric:
    df[i] = pd.to_numeric(df[i])
df.loc[kg, "Вес"] = df.loc[kg,"Вес"]*1000
df = df[
    [
    'Название', 'Вес','Ссылка', 'СтараяЦена',
    'Цена',  'Состав', 'Изготовитель', 'Марка', 
    'СрокГодности','ТемператураХранения', 
    'ЭнергетическаяЦенность','Белки', 'Углеводы', 'Жиры'
    ]
]
df.Состав = df.Состав.str.replace(".(.*?):", "")
df.Состав = df.Состав.str.replace("[\(]", ", ")
df.Состав = df.Состав.str.replace("[\)]", "")
df.Состав = df.Состав.str.split(",").apply(lambda x: [y.strip() for y in x])


# In[274]:


df[df.Марка.str.contains("Beyod Mea")]
df.Марка = df.Марка.replace({"Beyod Mea": "Beyond Meat"})


# In[263]:





# In[282]:


import itertools

состав = df.Состав.to_list()
состав = list(itertools.chain.from_iterable(состав))


# In[284]:


get_ipython().system('pip install wordcloud')


# In[297]:


import os

from os import path
from wordcloud import WordCloud

# # Generate a word cloud image
# wordcloud = WordCloud(width=4000, height=4000, background_color="white").generate(" ".join(состав))

# # Display the generated image:
# # the matplotlib way:
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")

# lower max_font_size
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [100, 80]

wordcloud = WordCloud(width=1000, height=800, background_color="white").generate(" ".join(состав))
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# In[299]:


len(состав)
(set(состав)


# In[301]:


from collections import Counter
состав = Counter(состав)


# In[303]:


слова_состав = list(состав)


# In[306]:


for ин in слова_состав:
    df[ин] = df["Состав"].contains(ин)


# In[308]:


ddf = df.explode("Состав")


# In[311]:


ddf = ddf.Состав.str.get_dummies()


# In[317]:


ddf = ddf.reset_index()
ddf = ddf.groupby("index").sum()


# In[319]:


ddf = ddf.reset_index(drop=True)


# In[320]:


df.join(ddf)


# In[330]:


слова_состав = ddf.columns[1:]


# In[328]:


df[ddf.columns[1:]] = ddf[ddf.columns[1:]]


# In[336]:


df.columns[10:20]


# In[338]:


df["ЦенаЗаГрамм"] = pd.to_numeric(df.Цена, "coerce")/df.Вес
df["ВсегоБелка"] = pd.to_numeric(df.Белки, "coerce")/100 * df.Вес
df["ВсегоУглеводов"] = pd.to_numeric(df.Углеводы, "coerce")/100 * df.Вес
df["ВсегоЖиров"] = pd.to_numeric(df.Жиры, "coerce")/100 * df.Вес


# In[339]:


df.to_csv("данные.csv")

