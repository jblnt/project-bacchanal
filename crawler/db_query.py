from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_exec import Articles, Base

engine=create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)

dbSession=sessionmaker(bind=engine)
session=dbSession()

def articleQuery_all():
    return session.query(Article).all()

for p in articleQuery_all():
    print(p.id, p.title, p.date)