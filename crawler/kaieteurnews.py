from article import Article_obj
from bs4 import BeautifulSoup
from datetime import date
from django.utils.text import slugify
from random import random
from requests import get, codes
from time import sleep
import images as imgFunc
import db_insert
import db_time
import sys

'''
def enc(string):
    st = string.replace('\xa0',' ')
    return st.encode('ascii', 'xmlcharrefreplace').decode('utf_8')
'''

def get_raw_html(site):
    r = get(site)

    if (r.status_code == codes.ok):
        return r.text
    else:
        raise Exception("Error Occured getting HTML. Error Code: {}".format(r.status_code))

def scrapePages(url):
    pagesArray=[]
    
    soup=BeautifulSoup(get_raw_html(url), 'html.parser')
    mainPages=soup.find("div", class_="pagination")
    
    if mainPages == None:
        return pagesArray 

    linkElements=mainPages.find_all("a")
    
    for index in range(len(linkElements)-1):
        pagesArray.append(linkElements[index].get("href"))

    return pagesArray

def scrapeContent(url):
    soup=BeautifulSoup(url, 'html.parser')    
    mainArticleDiv=soup.body.find("div", class_="sidebar_content")
    
    paragraphs=""
    images=[]
    
    for sibling in mainArticleDiv.div.div.div.find("p").next_siblings:
        #gets text data from p tags of article
        if sibling.name == "p": 
            paragraphs+=sibling.get_text().strip()+" <br>"
        
        if str(type(sibling)) != "<class 'bs4.element.NavigableString'>":
            #gets image data from img tags of article
            images += imgFunc.scrapeArticleImages(sibling)

    caption=mainArticleDiv.div.div.div.find("p").find("span", "meta-cat").a.get_text()
  
    #p = enc(paragraphs)
    p=paragraphs

    return p, caption, (",".join(images))

def scrapeArticles(url, articleDate):    
    beauObj=BeautifulSoup(get_raw_html(url), 'html.parser')
    articleList=beauObj.find_all("div", "post-news")

    articles=[]
    for link in articleList:
        articleTitle = link.find("h3").get_text()
        #articleTitle = enc(link.find("h3").get_text())
        articleLink = link.find("h3").a["href"]

        articleContent, articleCat, articleImages=scrapeContent(get_raw_html(articleLink))

        #Slug setup
        articleSlug=slugify(articleTitle)

        #image default
        if len(articleImages) == 0:
            articleImages="none"

        articles.append(Article_obj(articleTitle, articleSlug, articleContent, articleCat, "kaieteurnewsonline.com", articleDate, articleImages))

        #// Attempt to prevent Slamming Server...
        sec=5
        #sec="{:.1f}".format(random()*10)
        print("Sleeing for {} seconds.".format(sec))
        sleep(sec)
        #sleep(float(sec))
        #//

    return articles

def main():
    day = db_time.cur_day()
    month = db_time.cur_month()
    year = db_time.cur_year()
    
    print("scraping the {}, {}, {}".format(year, month, day))

    url="https://www.kaieteurnewsonline.com/{}/{:0d}/{:0d}/".format(year, month, day)
    pages=[url] + scrapePages(url)
    
    daily_article_objs=[]
    for page in pages:
        daily_article_objs += scrapeArticles(page, date(year, month, day))

    #db insert and commit
    for art in daily_article_objs:
        try:
            #print(art)
            db_insert.articleDBInsert(art.title, art.slug, art.content, art.tag, art.source, art.date, art.images)
            db_insert.session.commit()
        except Exception as e:
            print(art)
            print(e)
            db_insert.session.rollback()
            continue 

if __name__=="__main__":
    main()
