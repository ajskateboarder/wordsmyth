from typing import List

from fastapi import APIRouter, Query

from src.ytd import download_comments
from src.api.models.ytcom import YTComment

router = APIRouter()


@router.get("/func/ytscrape", response_model=List[YTComment])
def read(yt_id: str = Query()):
    return download_comments(f"https://youtube.com/watch?v={yt_id}", 0)
