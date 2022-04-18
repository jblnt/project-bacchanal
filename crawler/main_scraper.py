from article import Article_obj
from bs4 import BeautifulSoup
from datetime import date
from django.utils.text import slugify
from requests import get, codes
from time import sleep
import images as imgFunc
import db_insert
import db_time
import sys

def get_raw_html(site):
    r = get(site)

    if (r.status_code == codes.ok):
        return r.text
    else:
        return r.status_code
        #raise Exception("Error Occured getting HTML. Error Code: {}".format(r.status_code))

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

def scrapeContent(url, mode):
    soup = BeautifulSoup(url, 'html.parser')
    
    paragraphs=""
    images=[]

    if mode == "kn":
        mainArticleDiv=soup.body.find("div", class_="sidebar_content")

        family = mainArticleDiv.div.div.div.find("p").next_siblings

        caption = mainArticleDiv.div.div.div.find("p").find("span", "meta-cat").a.get_text()

    elif mode == "sn":
        mainArticleDiv=soup.body.find("main", class_="single-article")

        images+=imgFunc.headerImg(mainArticleDiv.div.div.article.header)

        try:
            family = mainArticleDiv.find("div", class_="article-content").children
        except:
            family = mainArticleDiv.find("div", class_="page-content").children
        
        caption = mainArticleDiv.find("div", "article-head").div.a.get_text()

    else:
        print("Invalid Mode Scraping Article")
        sys.exit()
    
    for sibling in family:
        #gets text data from p tags of article
        if sibling.name == "p": 
            paragraphs += sibling.get_text().strip()+" <br>"
        
        if str(type(sibling)) != "<class 'bs4.element.NavigableString'>":
            #gets image data from img tags of article
            images += imgFunc.scrapeArticleImages(sibling)
    
    if caption.strip() == "Guyana News":
        caption = "News"
    
    p = paragraphs

    return p, caption, (",".join(images))

def scrapeArticles(url, articleDate, mode):
    main_html_result = get_raw_html(url)
    
    if (main_html_result == 404):
        print("Page not Found... {}".format(main_html_result))
        return
    
    beauObj=BeautifulSoup(main_html_result, 'html.parser')

    if mode == "kn":
        articleList = beauObj.find_all("div", "post-news")
        ar_list = articleList

    elif mode == "sn":
        articleList = beauObj.find("div", class_="day-archives")
        ar_list = articleList.contents #children

    else:
        print("Invalid Mode Scraping Article List")
        sys.exit()

    articles=[]

    counter = 1
    article_list_count = len(ar_list)
    
    for link in ar_list:
        if mode == "kn":
            articleTitle = link.find("h3").get_text()

            articleLink = link.find("h3").a["href"]

            articleSource = "kaieteurnewsonline.com"

        elif mode  == "sn":
            articleTitle = link.find("h2").get_text()

            articleLink = link.find("h2").a["href"]

            articleSource = "stabroeknews.com"

        else:
            print("Invalid Mode")
            sys.exit()

        article_html_result = get_raw_html(articleLink)        
        if (article_html_result == 404):
            print("Article not Found... {}".format(article_html_result))
            continue

        articleContent, articleCat, articleImages=scrapeContent(article_html_result, mode)

        #create slug for links
        articleSlug=slugify(articleTitle)

        if len(articleImages) == 0:
            articleImages="none"

        #append new article object
        articles.append(Article_obj(articleTitle, articleSlug, articleContent, articleCat, articleSource, articleDate, articleImages))

        #// Attempt to prevent Slamming Server...
        if counter != article_list_count:
            sec = 4
            print("Sleeping for {} seconds. {} / {} complete".format(sec, counter, article_list_count))
            sleep(sec)
            counter += 1
        else:
            print("Finiahsed. {} / {}".format(counter, article_list_count))
        #//

    return articles

def main():
    day = db_time.cur_day()
    month = db_time.cur_month()
    year = db_time.cur_year()

    print("Scraping Archives from {}, {}, {}".format(day, month, year))

    #news sources from which i will be scraping.
    sources={'kn': 'https://www.kaieteurnewsonline.com/', 'sn': 'https://www.stabroeknews.com/'}

    #iterate over the entires within the sources dict.
    daily_article_objs=[]
    
    for k in sources:
        url = sources[k] + "{}/{:0d}/{:0d}/".format(year, month, day)
        mode = k
        #print(url)

        if mode == "kn":
            pages=[url] + scrapePages(url)

            #daily_article_objs=[]
            for page in pages:
                daily_article_objs += scrapeArticles(page, date(year, month, day), mode)

        elif mode == "sn":
            daily_article_objs += scrapeArticles(url, date(year, month, day), mode)

        else:
            print("Invalid Mode")
            sys.exit()

    #for i in daily_article_objs:
        #print(i)
    
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
