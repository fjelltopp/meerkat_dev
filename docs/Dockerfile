FROM buildpack-deps:jessie

# Set things up
ENV LANG C.UTF-8
ENV MINICONDA_PACKAGE Miniconda3-4.3.11-Linux-x86_64.sh
ENV PYT_VERSION python3.6
ENV PATH /miniconda/bin:${PATH}
ENV PYTHONPATH /miniconda/lib/{PYT_VERSION}/site-packages

RUN apt-get update &&\
    apt-get -y install postgresql-client libpq-dev libgeos-c1 &&\
    apt-get clean

# Install MiniConda package manage and pandas
RUN curl -LO https://repo.continuum.io/miniconda/${MINICONDA_PACKAGE} &&\
    bash ${MINICONDA_PACKAGE} -p /miniconda -b &&\
    rm ${MINICONDA_PACKAGE} &&\
    conda update -y conda &&\
    conda install -y pandas

RUN pip install git+https://github.com/lunant/sphinxcontrib-autojs.git

WORKDIR /var/www

# Install pip requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip install -r libs_req.tmp && rm libs_req.tmp

ADD meerkat_api/api_background/requirements.txt apiback_req.tmp
RUN pip install -r apiback_req.tmp && rm apiback_req.tmp

ADD meerkat_api/requirements.txt api_req.tmp
RUN pip install -r api_req.tmp && rm api_req.tmp

ADD meerkat_frontend/requirements.txt frontend_req.tmp
RUN pip install -r frontend_req.tmp && rm frontend_req.tmp

ADD meerkat_abacus/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp && rm abacus_req.tmp

ADD meerkat_auth/requirements.txt auth_req.tmp
RUN pip install -r auth_req.tmp && rm auth_req.tmp

ADD meerkat_hermes/requirements.txt hermes_req.tmp
RUN pip install -r hermes_req.tmp && hermes_req.tmp

# Add packages to the python path after installing dependancies. Make it easier to add a new package.
ENV PYTHONPATH ${PYTHONPATH}:/var/www/meerkat_auth/meerkat_auth:/var/www/meerkat_abacus/:/var/www/meerkat_libs:/var/www/meerkat_api:/var/www/meerkat_api/api_background:/var/www/meerkat_frontend:/var/www/meerkat_hermes
WORKDIR /var/www/meerkat_docs
ADD start-up /usr/bin/start-up

CMD ["start-up"]
