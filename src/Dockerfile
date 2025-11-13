FROM python:3.13.7

WORKDIR /srs

COPY . /srs

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt