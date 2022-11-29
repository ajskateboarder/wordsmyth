FROM python:3.9-bullseye

WORKDIR /app

COPY ./src /app/src
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg
COPY ./requirements.txt /app/requirements.txt

# install torch cpu
RUN pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -U --no-cache-dir -r /app/requirements.txt

RUN wget https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0# -O /app/src/algorithms/deepmoji/model/pytorch_model.bin

ENV PORT 50051
CMD ["python3", "src/interns/server.py"]