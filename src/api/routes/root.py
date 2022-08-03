from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def read():
    return "Pong.\n"
