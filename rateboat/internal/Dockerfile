FROM python:3.9-slim

WORKDIR /app

COPY ./rateboat /app/rateboat
COPY ./setup.py /app/setup.py
COPY ./setup.cfg /app/setup.cfg

RUN apt update && apt install --no-install-recommends -y wget git
RUN wget https://www.dropbox.com/s/q8lax9ary32c7t9/pytorch_model.bin?dl=0# -O /app/rateboat/algorithms/deepmoji/model/pytorch_model.bin
RUN pip install -f https://download.pytorch.org/whl/torch_stable.html torch==1.13.1+cpu \
    && cat rateboat/internal/requirements.txt | xargs --max-args=1 --max-procs=4 pip install -U --no-cache-dir || true

ENV PORT 50051
CMD ["python3", "rateboat/internal/server.py"]