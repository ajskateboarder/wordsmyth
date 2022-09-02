"""Strings all the routes together into a single app"""

from fastapi import FastAPI

from src.micro.routes import deepmoji_predict, roberta_predict, root

app = FastAPI()

app.include_router(root.router)

app.include_router(deepmoji_predict.router)
app.include_router(roberta_predict.router)
