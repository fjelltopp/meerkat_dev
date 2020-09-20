FROM python:3.7

RUN apt-get update &&\
    apt-get -y install postgresql-client libpq-dev libgeos-c1v5 &&\
    apt-get clean

# Install pip requirements. Add requirements list to bust-cache if any changes.
WORKDIR /var/www
ADD meerkat_libs/requirements.txt libs_req.txt
RUN pip3 install -r libs_req.txt && rm libs_req.txt

ADD meerkat_logging/requirements.txt logging_req.txt
RUN pip3 install -r logging_req.txt && rm logging_req.txt

ENV PYTHONPATH=${PYTHONPATH}:/var/www/meerkat_libs

ADD meerkat_dev/logging/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/logging/start-up /usr/bin/start-up

WORKDIR /var/www/meerkat_logging

CMD ["start-up"]
