FROM debian:buster

RUN apt-get update
RUN apt-get -y install curl bzip2 build-essential postgresql-client libpq-dev libgeos-c1v5 python3 python3-pip
RUN apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

WORKDIR /var/www

# Install pip requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip install -r libs_req.tmp

ADD meerkat_abacus/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp &&\
    rm *_req.tmp

ADD meerkat_api/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp &&\
    rm *_req.tmp

ENV PYTHONPATH /var/www/meerkat_libs:/var/www/meerkat_api/api_background:/var/www/meerkat_abacus

#Copy the start up script and setup working directory.
COPY meerkat_dev/abacus/start_consumer.sh /usr/bin/start_consumer
COPY meerkat_dev/abacus/start_pipeline.sh /usr/bin/start_pipeline
COPY meerkat_dev/abacus/start_api_background.sh /usr/bin/start_api_background
