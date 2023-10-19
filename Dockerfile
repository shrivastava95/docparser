FROM ubuntu:latest 
LABEL maintainer="rexdivakar"

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV DEBIAN_FRONTEND=noninteractive
# RUN python -m venv /opt/venv
# ENV PATH="/opt/venv/bin:$PATH"


# update binaries & install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository --yes ppa:alex-p/tesseract-ocr5 \
    && apt-get update \
    && apt-get -y install git poppler-utils tesseract-ocr python3 python3-pip\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN tesseract --version

ADD . /code
WORKDIR /code


# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

RUN pip install git+https://github.com/openai/CLIP.git

# RUN python3 /code/test_doc.py