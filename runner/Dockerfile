FROM buildpack-deps:jessie

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV MINICONDA_PACKAGE Miniconda3-4.3.11-Linux-x86_64.sh
ENV PYT_VERSION python3.6

RUN apt-get update &&\
    apt-get -y install postgresql-client libpq-dev libgeos-c1 &&\
    apt-get clean

ENV PATH=/miniconda/bin:${PATH}
ENV PYTHONPATH=/miniconda/lib/{PYT_VERSION}/site-packages
RUN curl -LO https://repo.continuum.io/miniconda/${MINICONDA_PACKAGE} &&\
    bash ${MINICONDA_PACKAGE} -p /miniconda -b &&\
    rm ${MINICONDA_PACKAGE} &&\
    conda update -y conda &&\
    conda install -y pandas

RUN mkdir -p /var/www/meerkat_runner
WORKDIR /var/www

# Install pip requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip install -r libs_req.tmp

ADD meerkat_api/api_background/requirements.txt api_req.tmp
RUN pip install -r api_req.tmp

ADD meerkat_runner/requirements.txt runner_req.tmp
RUN pip install -r runner_req.tmp

ADD meerkat_abacus/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp &&\
    rm *_req.tmp

WORKDIR /var/www/meerkat_runner

COPY meerkat_runner/requirements.txt /var/www/meerkat_runner/requirements.txt
RUN pip install -r requirements.txt


COPY meerkat_dev/runner/start_celery /usr/bin/start_celery
WORKDIR /var/www/meerkat_runner
CMD ["start_celery"]
