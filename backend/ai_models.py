from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment"
)

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


def analyze_sentiment(text):

    if not text:
        return "neutral", 0

    result = sentiment_model(text[:512])[0]

    label = result["label"]

    if label == "LABEL_0":
        return "negative", result["score"]

    if label == "LABEL_1":
        return "neutral", result["score"]

    return "positive", result["score"]


def summarize(text):

    if not text or len(text) < 200:
        return text

    summary = summarizer(
        text[:1024],
        max_length=80,
        min_length=30,
        do_sample=False
    )

    return summary[0]["summary_text"]