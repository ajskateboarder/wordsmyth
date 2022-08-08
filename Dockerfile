FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -U -r /app/requirements.txt

COPY ./src /app/src

ENV PORT 8000
CMD ["sh", "-c", "uvicorn src:app --host 0.0.0.0 --port ${PORT}"]