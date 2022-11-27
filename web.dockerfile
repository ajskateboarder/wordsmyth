FROM python:3.9-bullseye

WORKDIR /app

COPY ./src /app/src
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN pip install pika
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /app/wait.sh
RUN chmod +x /app/wait.sh

CMD ["python3", "src/web/backend.py"]