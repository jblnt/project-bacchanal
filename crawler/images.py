from requests import get
from bs4 import BeautifulSoup

def fetch_img(sibling):
    images=[]

    for img in sibling.find_all("img"):
        try:
            srcset=img["srcset"]
            src=sorted(srcset.replace(", ",",").split(","))[-1].split()[-2]
            #images.append(sorted(srcset.replace(", ",",").split(","))[-1].split()[-2])
            #print(src)

        except:
            #images.append(img["src"])
            src=img["src"]
        
        if (src[:4] == "http"):
            #print(src)
            images.append(src)

    return images

def headerImg(tag):
    try:
        return fetch_img(tag.figure.a.noscript)
        #return [tag.figure.a.noscript.img["src"]]        
    except:
        return []

#main function call
def scrapeArticleImages(sibling):
    img_tag=[]

    if sibling.name=="p" or sibling.name=="figure": 
        img_tag+=fetch_img(sibling)

        #if f_img != None:
        #    images.append(f_img)

    if sibling.name == "div" and sibling.has_attr('class'):
        classes=sibling['class']
        for i in range(len(classes)):
            if classes[i] == "wp-caption" or classes[i] == "photo-item":
                img_tag+=fetch_img(sibling)

    return (img_tag)

def updateScrape(url):
    soup=BeautifulSoup(get(url).text, 'html.parser')    
    mainArticleDiv=soup.body.find("div", class_="sidebar_content")
    
    images=[]
    for sibling in mainArticleDiv.div.div.div.find("p").next_siblings:

        #gets image data from slice of article
        if str(type(sibling)) != "<class 'bs4.element.NavigableString'>":
            #gets image data from slice of article
            images += scrapeArticleImages(sibling)

    return images