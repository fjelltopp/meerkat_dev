FROM debian:jessie

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
ENV MINICONDA_PACKAGE Miniconda3-4.3.11-Linux-x86_64.sh
ENV PYT_VERSION python3.6

RUN apt-get update &&\
    apt-get -y install tk-dev curl postgresql-client libpq-dev libgeos-c1 &&\
    apt-get clean

ENV PATH=/miniconda/bin:${PATH}
ENV PYTHONPATH=/miniconda/lib/${PYT_VERSION}/site-packages

RUN curl -LO https://repo.continuum.io/miniconda/${MINICONDA_PACKAGE}
RUN bash ${MINICONDA_PACKAGE} -p /miniconda -b
RUN rm ${MINICONDA_PACKAGE}
RUN conda update -y conda
RUN conda install -y pandas
RUN pip install uwsgi

RUN mkdir -p /var/www/meerkat_api
WORKDIR /var/www

# Install pip requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip install -r libs_req.tmp
ADD meerkat_abacus/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp
ADD meerkat_api/api_background/requirements.txt apiback_req.tmp
RUN pip install -r apiback_req.tmp
ADD meerkat_analysis/requirements.txt analysis_req.tmp
RUN pip install -r analysis_req.tmp
ADD meerkat_api/requirements.txt api_req.tmp
RUN pip install -r api_req.tmp

# Add all above dependancies to the python path.  Do it late in the process so it is easy to change without breaking cache.
ENV PYTHONPATH=${PYTHONPATH}:/var/www/meerkat_libs:/var/www/meerkat_abacus:/var/www/meerkat_api/api_background:/var/www/meerkat_analysis
ADD meerkat_dev/api/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/api/run /usr/bin/run
WORKDIR /var/www/meerkat_api

CMD ["run"]
