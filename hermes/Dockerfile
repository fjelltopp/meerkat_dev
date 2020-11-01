FROM python:3.7

RUN apt-get update

WORKDIR /var/www/meerkat_hermes

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

ADD meerkat_hermes/requirements.txt /var/www/meerkat_hermes/requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONPATH=/var/www/meerkat_libs

ADD meerkat_dev/hermes/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/hermes/run /usr/bin/run

CMD ["run"]
