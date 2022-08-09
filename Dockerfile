FROM python:3.9-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -U -r /app/requirements.txt

COPY ./src /app/src
RUN python3 -c 'from torchmoji.dl_utils import execute_download; execute_download("/app/src/deepmoji/model/pytorch_model.bin")'
RUN ls

ENV PORT 8000
CMD ["sh", "-c", "uvicorn src:app --host 0.0.0.0 --port ${PORT}"]