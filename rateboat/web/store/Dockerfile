FROM python:3.9-alpine

WORKDIR /app

COPY ./rateboat /app/rateboat
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN apk update && apk add python3-dev git
RUN pip install --no-cache-dir -U -r /app/rateboat/web/store/requirements.txt

ENV PORT 50056
CMD ["python3", "rateboat/web/store/server.py"]