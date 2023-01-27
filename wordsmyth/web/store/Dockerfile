FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && apk add --no-cache git

COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg
COPY ./requirements/store.txt /app/requirements.txt
RUN pip install --no-cache-dir -U -r /app/requirements.txt

COPY ./wordsmyth /app/wordsmyth

CMD ["rq", "worker"]