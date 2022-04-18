from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, Date, Text, CHAR
import json

#Read environment JSON file
with open('/python/project-bacchanal/secrets.json') as env:
    config = json.load(env)

Base=declarative_base()

class Articles(Base):
    __tablename__='articles'

    id=Column(Integer, primary_key=True, autoincrement='auto', nullable=False)

    title=Column(VARCHAR(length=256), nullable=False)
    slug=Column(VARCHAR(length=256), nullable=False)
    content=Column(Text)
    tag=Column(VARCHAR(length=128))
    source=Column(VARCHAR(length=128), nullable=False)
    date=Column(Date, nullable=False)
    images=Column(Text, nullable=False)

url = "postgresql+psycopg2://{}:{}@{}:{}/django".format(config["RDS_USERNAME"], config["RDS_PASSWORD"], config["RDS_HOSTNAME"], config["RDS_PORT"])
engine = create_engine(url)

Base.metadata.create_all(engine)
