"""Strings all the routes together into a single app"""

from fastapi import FastAPI

from src.micro.routes import predict, root

app = FastAPI()

app.include_router(root.router)
app.include_router(predict.router)
