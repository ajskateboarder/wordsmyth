FROM python:3.8

COPY requirements.txt /app/
COPY wordsmyth-0.1-py3-none-any.whl /app/

RUN pip install -r /app/requirements.txt
RUN pip install /app/wordsmyth-0.1-py3-none-any.whl

COPY . /app

CMD ["python", "/app/main.py"]