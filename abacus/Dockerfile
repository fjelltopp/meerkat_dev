FROM buildpack-deps:jessie

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV MINICONDA_PACKAGE Miniconda3-4.3.11-Linux-x86_64.sh
ENV PYT_VERSION python3.6
ENV PATH /miniconda/bin:${PATH}
ENV PYTHONPATH /miniconda/lib/{PYT_VERSION}/site-packages

RUN apt-get update &&\
    apt-get -y install postgresql-client libpq-dev libgeos-c1 &&\
    apt-get clean

# Install miniconda, which comes with its own version of python3.
RUN curl -LO https://repo.continuum.io/miniconda/${MINICONDA_PACKAGE} &&\
    bash ${MINICONDA_PACKAGE} -p /miniconda -b &&\
    rm ${MINICONDA_PACKAGE} &&\
    conda update -y conda &&\
    conda install -y pandas

WORKDIR /var/www/meerkat_abacus
ADD requirements.txt /var/www/meerkat_abacus/requirements.txt
RUN pip install -r requirements.txt

COPY start_celery /usr/bin/start_celery
CMD ["start_celery"]
