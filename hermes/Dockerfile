FROM python:3.7

RUN apt-get update
RUN pip3 install uwsgi

WORKDIR /var/www/meerkat_hermes

ADD meerkat_hermes/requirements.txt /var/www/meerkat_hermes/requirements.txt
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/var/www/meerkat_libs

ADD meerkat_dev/hermes/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/hermes/run /usr/bin/run

CMD ["run"]
