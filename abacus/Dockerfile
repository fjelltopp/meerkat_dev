FROM debian:jessie

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV MINICONDA_PACKAGE Miniconda3-4.3.11-Linux-x86_64.sh
ENV PYT_VERSION python3.6
ENV PATH /miniconda/bin:${PATH}

RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update
RUN apt-get -y install curl bzip2 build-essential postgresql-client libpq-dev libgeos-c1
RUN apt-get clean

# Install miniconda, which comes with its own version of python3.
RUN curl -LO https://repo.continuum.io/miniconda/${MINICONDA_PACKAGE} &&\
    bash ${MINICONDA_PACKAGE} -p /miniconda -b &&\
    rm ${MINICONDA_PACKAGE} &&\
    conda update -y conda &&\
    conda install -y pandas

WORKDIR /var/www

# Install pip requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip install -r libs_req.tmp

ADD meerkat_abacus/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp &&\
    rm *_req.tmp

ADD meerkat_api/api_background/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp &&\
    rm *_req.tmp


ENV PYTHONPATH /miniconda/lib/{PYT_VERSION}/site-packages:/var/www/meerkat_libs:/var/www/meerkat_api/api_background:/var/www/meerkat_abacus

#Copy the start up script and setup working directory.
COPY meerkat_dev/abacus/start_pipeline.sh /usr/bin/start_pipeline
COPY meerkat_dev/abacus/start_consumer.sh /usr/bin/start_consumer
COPY meerkat_dev/abacus/start_api_background.sh /usr/bin/start_api_background
