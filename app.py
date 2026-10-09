from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: list[str]

POSITIVE = set("""
love loved lovely like liked great excellent amazing awesome
wonderful fantastic good happy joy joyful best beautiful perfect
enjoy enjoyed delightful brilliant superb excited pleased success
helpful impressive recommend fun glad satisfied positive kind
friendly thankful excellent nice outstanding valuable better
""".split())

NEGATIVE = set("""
hate hated terrible awful horrible bad sad angry upset
disappointed disappointing worst poor boring annoying annoyed
ugly fail failed failure broken useless dislike painful frustrating
frustrated unhappy miserable depressing disgusting regret problem
problems wrong difficult negative stressful pathetic unfortunate
inferior worse unpleasant scary scary
""".split())

NEGATIONS = {
    "not", "never", "no", "neither", "hardly", "isn't",
    "wasn't", "don't", "doesn't", "didn't", "cannot",
    "can't", "couldn't", "won't", "wouldn't"
}

def classify(sentence: str) -> str:
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", sentence.lower())
    score = 0
    negate = 0

    for word in words:
        if word in NEGATIONS:
            negate = 3
            continue

        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0

        if value:
            score += -value if negate > 0 else value

        if negate > 0:
            negate -= 1

    if score > 0:
        return "happy"
    if score < 0:
        return "sad"
    return "neutral"

@app.get("/")
async def root():
    return {"message": "Batch Sentiment API is running"}

@app.post("/sentiment")
async def sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": classify(sentence)
            }
            for sentence in request.sentences
        ]
    }
