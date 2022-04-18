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
    st=string.replace('\xa0', ' ')
    return st.encode('ascii', 'xmlcharrefreplace').decode('utf_8')
'''

def get_raw_html(site):
    r = get(site)

    if (r.status_code == codes.ok):
        return r.text
    else:
        return r.status_code
        #raise Exception("Error Occured getting HTML. Error Code: {}".format(r.status_code))

def scrapeContent(urlText):
    soup=BeautifulSoup(urlText, 'html.parser')    
    mainArticleDiv=soup.body.find("main", class_="single-article")
    
    paragraphs=""
    images=[]

    #grab stabroke header img. if any.
    images+=imgFunc.headerImg(mainArticleDiv.div.div.article.header)

    try:
        children=mainArticleDiv.find("div", class_="article-content").children
    except:
        children=mainArticleDiv.find("div", class_="page-content").children

    for sibling in children:
        #gets text data from p tags of article
        if sibling.name=="p": 
            paragraphs+=sibling.get_text().strip()+" <br>"
        
        if str(type(sibling)) != "<class 'bs4.element.NavigableString'>":
            #gets image data from img tags of article
            images += imgFunc.scrapeArticleImages(sibling)

    caption=mainArticleDiv.find("div", "article-head").div.a.get_text()

    if caption.strip() == "Guyana News":
        caption = "News"

    #p = enc(paragraphs)
    p = paragraphs

    return p, caption, (",".join(images))

def scrapeArticles(url, articleDate):    
    beauObj=BeautifulSoup(get_raw_html(url), 'html.parser')
    articleList=beauObj.find("div", class_="day-archives")

    articles=[]
    for link in articleList.children:
        articleTitle=link.find("h2").get_text()
        #articleTitle=enc(link.find("h2").get_text())
        
        articleLink=link.find("h2").a["href"]
        
        article_html_result = get_raw_html(articleLink)
        
        if (article_html_result == 404):
            print("Article not Found... {}".format(article_html_result))
            continue

        articleContent, articleCat, articleImages=scrapeContent(article_html_result)

        #Slug setup
        articleSlug=slugify(articleTitle)

        #image default
        if len(articleImages) == 0:
            articleImages="none"
        
        articles.append(Article_obj(articleTitle, articleSlug, articleContent, articleCat, "stabroeknews.com", articleDate, articleImages))

        #// Attempt to prevent Slamming Server...
        sec=5
        print("Sleeing for {} seconds.".format(sec))
        sleep(sec)
        #//

    return articles

def main():    
    day = db_time.cur_day()
    month = db_time.cur_month()
    year = db_time.cur_year()

    print("scraping the {}".format(day))

    url="https://www.stabroeknews.com/{}/{:0d}/{:0d}/".format(year, month, day)

    daily_article_objs=scrapeArticles(url, date(year, month, day))
   
    #db insert and commit
    for art in daily_article_objs:
        db_insert.articleDBInsert(art.title, art.slug, art.content, art.tag, art.source, art.date, art.images)

    db_insert.session.commit()

if __name__=="__main__":
    main()
