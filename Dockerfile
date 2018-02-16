FROM python:3

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

#RUN apt-get update -y && apt-get install mysql-server -y

COPY . /usr/src/app

EXPOSE 8000
CMD ["uwsgi", "--http", ":8000", "--module", "ppsus.wsgi"]