FROM python:3.9-alpine

WORKDIR /app
RUN apk add wget git gcc g++ gfortran openblas python3-dev

COPY ./rateboat /app/rateboat
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN wget https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0# -O /app/rateboat/algorithms/deepmoji/model/pytorch_model.bin
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -U -r ./rateboat/internal/requirements.txt

ENV PORT 50051
CMD ["python3", "rateboat/internal/server.py"]