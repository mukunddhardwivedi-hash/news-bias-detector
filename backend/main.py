from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Article
from fetch_news import fetch_all
from ai_models import analyze_sentiment, summarize
from article_extractor import extract_article

app = FastAPI()
@app.post("/fetch")
def fetch_and_store(db: Session = Depends(get_db)):
    articles = fetch_all()
    added = 0

    for a in articles:
        # 1. Check if it already exists to avoid duplicate heavy processing
        exists = db.query(Article).filter_by(url=a["url"]).first()

        if exists or not a["title"] or not a["url"]:
            continue

        try:
            # 2. Extract full text content from the URL
            content = extract_article(a["url"])
            
            # 3. Generate summary and analyze sentiment based on the full CONTENT
            # (Note: Ensure analyze_sentiment handles long text or truncates it)
            summary = summarize(content)
            sentiment, score = analyze_sentiment(content)

            # 4. Create the Database object
            article = Article(
                title=a["title"],
                source=a["source"],
                url=a["url"],
                published=a.get("published"),
                content=content,
                summary=summary,
                bias=a["bias"],
                sentiment=sentiment,
                sentiment_score=score,
            )

            db.add(article)
            added += 1
            
        except Exception as e:
            print(f"Error processing article {a['url']}: {e}")
            continue

    # Commit all new entries at once
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
            "summary": a.summary,
            "bias": a.bias,
            "sentiment": a.sentiment,
        }
        for a in articles
    ]