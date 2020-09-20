FROM python:3.7

RUN apt-get update

WORKDIR /var/www/meerkat_consul

ADD meerkat_consul/requirements.txt /var/www/meerkat_consul/requirements.tmp
RUN pip3 install -r requirements.tmp
ADD meerkat_libs/requirements.txt /var/www/meerkat_consul/lib_requirements.tmp
RUN pip3 install -r lib_requirements.tmp

ENV PYTHONPATH=/var/www/meerkat_libs

ADD meerkat_dev/consul/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/consul/run /usr/bin/run

CMD 'run'
