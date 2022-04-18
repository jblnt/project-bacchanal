from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_exec import Articles, Base, engine

Base.metadata.create_all(engine)

dbSession=sessionmaker(bind=engine)
session=dbSession()

def articleDBInsert(aTitle, aSlug, aContent, aTag, aSource, aDate, aImages):
    new_article=Articles(title=aTitle, slug=aSlug, content=aContent, tag=aTag, source=aSource, date=aDate, images=aImages)
    session.add(new_article)
