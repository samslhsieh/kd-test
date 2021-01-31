FROM python:3.9.1-alpine3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        python3-dev \

#        for psycopg2
        musl-dev \

#        for drf-jwt
        libffi-dev \
    && apk add --no-cache \
#        for psycopg2, it can not be removed on runtime, but postgresql-dev too large
        'postgresql-dev<12.2-r0' \
#        postgresql-dev \
    && pip install --no-cache-dir \
        psycopg2 \
        drf-jwt \
        uwsgi \
    && apk del --no-cache .build-deps

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

#RUN LD_PRELOAD=/lib/libssl.so.1.1 python3 manage.py collectstatic