FROM python:3.9-alpine

WORKDIR /app

RUN apk update && apk add python3-dev git

COPY ./wordsmyth /app/wordsmyth
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg
COPY ./requirements/api.txt /app/requirements.txt
RUN pip install --no-cache-dir -U -r /app/requirements.txt

ENV PORT 8081
CMD ["uvicorn", "wordsmyth.web.api.main:app", "--port", "8081"]