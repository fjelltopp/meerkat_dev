FROM python:3.6

RUN apt-get update &&\
    apt-get -y install postgresql-client libpq-dev libgeos-c1 &&\
    apt-get clean &&\
    pip3 install uwsgi

WORKDIR /var/www/meerkat_logging

ADD meerkat_logging/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && rm requirements.txt

ADD meerkat_dev/logging/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/logging/start-up /usr/bin/start-up

CMD ["start-up"]
