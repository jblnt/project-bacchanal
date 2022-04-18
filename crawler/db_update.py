from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_exec import Articles, Base
import images as img

engine=create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)

dbSession=sessionmaker(bind=engine)
session=dbSession()

def articleDBUpdate(aID):
    article=session.query(Articles).filter_by(id=aID).first() 
    
    #urls=article.images
    #urls="https://www.kaieteurnewsonline.com/2020/02/24/guyana-celebrates-50-golden-years/"

    gatherNew=[]
    for url in urls.split(","):
        gatherNew+=img.updateScrape(url)

    #print(gatherNew)
    article.images=(",".join(gatherNew))
        
#borked ID'S
id=[369]

for i in id:
    articleDBUpdate(i)

print(session.dirty)
session.commit()