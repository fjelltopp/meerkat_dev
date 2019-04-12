FROM python:3.6.2

RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update &&\
    pip3 install uwsgi

WORKDIR /var/www/meerkat_consul

ADD meerkat_consul/requirements.txt /var/www/meerkat_consul/requirements.tmp
RUN pip3 install -r requirements.tmp
ADD meerkat_libs/requirements.txt /var/www/meerkat_consul/lib_requirements.tmp
RUN pip3 install -r lib_requirements.tmp

ENV PYTHONPATH=/var/www/meerkat_libs

ADD meerkat_dev/consul/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/consul/run /usr/bin/run

CMD 'run'
