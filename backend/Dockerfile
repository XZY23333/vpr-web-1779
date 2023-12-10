FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /backend

RUN apt update && \
    apt install -y python3 python3-pip libgl1-mesa-glx libglib2.0-0

COPY . /backend/

RUN pip3 install -r requirements.txt

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

CMD ["python3", "/backend/backend.py"]
