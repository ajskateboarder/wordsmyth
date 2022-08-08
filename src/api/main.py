from fastapi import FastAPI

from src.api.routes import predict, root

app = FastAPI()

app.include_router(root.router)
app.include_router(predict.router)
