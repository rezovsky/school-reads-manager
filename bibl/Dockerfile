FROM python:3.8.10-slim

RUN mkdir bibl
WORKDIR bibl

ADD requirements.txt /bibl/
RUN pip install -r requirements.txt
ADD .. /bibl/

ADD .docker.env /bibl/.env
ENV APP_NAME=BIBL

RUN pip3 install -r requirements.txt


CMD gunicorn bibl.wsgi:application -b 0.0.0.0:8000