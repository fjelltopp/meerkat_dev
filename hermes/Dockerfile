FROM python:3.6.2
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update
RUN pip3 install uwsgi

WORKDIR /var/www/meerkat_hermes

ADD meerkat_hermes/requirements.txt /var/www/meerkat_hermes/requirements.txt
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=/var/www/meerkat_libs

ADD meerkat_dev/hermes/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/hermes/run /usr/bin/run

CMD ["run"]
