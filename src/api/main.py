from fastapi import FastAPI

from src.api.routes.api import predict, ytscrape
from src.api.routes import root

app = FastAPI()

app.include_router(root.router)
app.include_router(predict.router)
app.include_router(ytscrape.router)
