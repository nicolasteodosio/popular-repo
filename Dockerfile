FROM python:3.8-alpine

RUN apk upgrade && \
  apk add --no-cache --virtual build-dependencies python3-dev linux-headers mysql-dev make gcc \
  g++ ca-certificates zlib-dev jpeg-dev tiff-dev freetype-dev lcms2-dev musl-dev \
  libwebp-dev tcl-dev tk-dev && \
  rm -rf /var/cache/apk/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt/code
WORKDIR /opt/code
RUN python -m pip install --upgrade pipenv wheel
RUN pipenv install --system
WORKDIR /opt/code/app
EXPOSE 8000