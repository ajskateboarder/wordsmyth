import os as _os
from dotenv import load_dotenv as _load_dotenv

_load_dotenv("env")

YTD_KEY = _os.environ.get("YTD_KEY")
