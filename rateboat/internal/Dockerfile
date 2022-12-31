FROM python:3.9-bullseye

WORKDIR /app

COPY ./rateboat /app/rateboat
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg
COPY ./requirements.txt /app/requirements.txt

# install torch cpu
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -U -r /app/requirements.txt

RUN wget https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0# -O /app/rateboat/algorithms/deepmoji/model/pytorch_model.bin

ENV PORT 50051
CMD ["python3", "rateboat/internal/server.py"]