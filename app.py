from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]


def classify(sentence: str) -> str:
    score = analyzer.polarity_scores(sentence)["compound"]

    if score >= 0.05:
        return "happy"
    elif score <= -0.05:
        return "sad"
    return "neutral"


def analyze(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify(sentence)
            }
            for sentence in request.sentences
        ]
    }


@app.get("/")
async def root():
    return {"message": "Batch Sentiment API is running"}


@app.post("/")
async def sentiment_root(request: SentimentRequest):
    return analyze(request)


@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    return analyze(request)
