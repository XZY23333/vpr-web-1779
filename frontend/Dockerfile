FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /frontend

RUN apt update && \
    apt install -y python3 python3-pip libgl1-mesa-glx libglib2.0-0

COPY . /frontend/

RUN pip3 install -r requirements.txt

CMD ["python3", "/frontend/frontend.py"]
