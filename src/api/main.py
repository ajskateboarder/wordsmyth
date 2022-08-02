import warnings

from fastapi import FastAPI, Header
from typing import Union
from src.deepmoji.deepmoj import Emojize

warnings.filterwarnings('ignore')

app = FastAPI()
emoji = Emojize()

@app.get('/')
def read_root():
    return "Hello world!!"

@app.get('/api/predictEmoji')
def read_predict_emoji(text: Union[str, None] = Header(default=None)):
    return {"emoji": emoji.predict(text)}