FROM python:3.8-slim-buster

ENV APP_HOME /app
ENV PYTHONUNBUFFERED 1
WORKDIR $APP_HOME
COPY . .

RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

CMD gunicorn --bind :$PORT --workers 1 --threads 8 mewgram.wsgi:application
