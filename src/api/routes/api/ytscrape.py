import time

from fastapi import APIRouter, Query

from src.ytd import download_comments
from src.api.models.ytcom import YTComment

router = APIRouter()


@router.get("/api/ytscrape", response_model=YTComment)
def read(yid: str = Query()):
    return download_comments(f"https://youtube.com/watch?v={yid}", 0)
