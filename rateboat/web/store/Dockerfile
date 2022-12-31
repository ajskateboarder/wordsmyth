FROM python:3.9-bullseye

WORKDIR /app

COPY ./ytstars /app/ytstars
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN pip install --no-cache-dir grpcio grpcio_tools requests
RUN pip install -e .

ENV PORT 50056
CMD ["python3", "ytstars/web/store/server.py"]