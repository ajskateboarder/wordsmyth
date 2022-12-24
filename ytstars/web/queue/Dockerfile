FROM python:3.9-bullseye

WORKDIR /app

COPY ./ytstars /app/ytstars
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN pip install pika requests grpcio grpcio_tools
RUN pip install -e .
RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -O /app/wait.sh
RUN chmod +x /app/wait.sh

CMD ["python3", "ytstars/web/queue/backend.py"]