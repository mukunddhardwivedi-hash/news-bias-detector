from sqlalchemy import Column, Integer, String, Text
from database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    source = Column(String)
    url = Column(String, unique=True)

    published = Column(String)

    content = Column(Text)     # FULL ARTICLE TEXT
    summary = Column(Text)     # AI SUMMARY

    bias = Column(String)

    sentiment = Column(String)
    sentiment_score = Column(String)