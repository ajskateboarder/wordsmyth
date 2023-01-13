FROM python:3.9-bullseye

WORKDIR /app

COPY ./rateboat /app/rateboat
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN pip install --no-cache-dir -U -r /app/rateboat/web/application/requirements.txt

ENV PORT 8081
CMD ["uvicorn", "rateboat.web.application.main:app", "--port", "8081"]