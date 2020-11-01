FROM debian:buster

RUN apt-get update
RUN apt-get -y install tk-dev curl postgresql-client libpq-dev libgeos-c1v5 python3 python3-pip
RUN apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

RUN mkdir -p /var/www/meerkat_api
WORKDIR /var/www

# Install pip3 requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip install -r libs_req.tmp
ADD meerkat_abacus/requirements.txt abacus_req.tmp
RUN pip install -r abacus_req.tmp
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
