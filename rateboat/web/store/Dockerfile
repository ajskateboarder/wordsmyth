FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update && apk add --no-cache git

COPY ./requirements/store.txt /app/requirements.txt
RUN pip install --no-cache-dir -U -r /app/requirements.txt

COPY ./rateboat /app/rateboat
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

CMD ["rq", "worker"]