FROM python:3.6.2

RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update &&\
    apt-get -y install postgresql-client libpq-dev libgeos-c1 &&\
    apt-get clean &&\
    pip3 install uwsgi

# Install pip requirements. Add requirements list to bust-cache if any changes.
WORKDIR /var/www
ADD meerkat_libs/requirements.txt libs_req.txt
RUN pip install -r libs_req.txt && rm libs_req.txt

ADD meerkat_logging/requirements.txt logging_req.txt
RUN pip3 install -r logging_req.txt && rm logging_req.txt

ENV PYTHONPATH=${PYTHONPATH}:/var/www/meerkat_libs

ADD meerkat_dev/logging/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/logging/start-up /usr/bin/start-up

WORKDIR /var/www/meerkat_logging

CMD ["start-up"]
