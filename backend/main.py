from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Article, Base, engine
from fetcher import fetch_all
from analyzer import analyze_sentiment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "News Bias API running"}

@app.post("/fetch")
def fetch_and_store(db: Session = Depends(get_db)):
    articles = fetch_all()
    added = 0

    for a in articles:
        exists = db.query(Article).filter_by(url=a["url"]).first()

        if exists or not a["title"] or not a["url"]:
            continue

        sentiment, score = analyze_sentiment(a["title"])

        article = Article(
            title=a["title"],
            source=a["source"],
            url=a["url"],
            published=a["published"],
            bias=a["bias"],
            sentiment=sentiment,
            sentiment_score=score,
        )

        db.add(article)
        added += 1

    db.commit()

    return {"added": added}

@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()

    return [
        {
            "title": a.title,
            "source": a.source,
            "url": a.url,
            "bias": a.bias,
            "sentiment": a.sentiment,
        }
        for a in articles
    ]