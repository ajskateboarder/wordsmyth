FROM python:3.9-slim

WORKDIR /app

RUN apt update && apt install --no-install-recommends -y wget git \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/
RUN pip install --no-cache-dir -f https://download.pytorch.org/whl/torch_stable.html torch==1.13.1+cpu

COPY ./requirements/internal.txt /app/requirements.txt
RUN cat /app/requirements.txt | xargs --max-args=1 --max-procs=4 pip install -U --no-cache-dir || true

COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg
COPY ./wordsmyth /app/wordsmyth
RUN pip install -e .

RUN wget https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0# -O /app/wordsmyth/algorithms/deepmoji/model/pytorch_model.bin

ENV PORT 50051

CMD ["python3", "wordsmyth/internal/server.py"]