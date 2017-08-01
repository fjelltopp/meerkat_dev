FROM python:3.6

# Install global requirements
ENV PYTHONPATH=/var/www/meerkat_libs
RUN wget -qO- https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get update &&\
    apt-get install -y nodejs gettext ghostscript &&\
    apt-get clean &&\
    pip3 install uwsgi
RUN npm install -g bower gulp yarn
WORKDIR /var/www

# Install pip requirements. Add requirements list to bust-cache if any changes.
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip3 install -r libs_req.tmp && rm libs_req.tmp
ADD meerkat_frontend/requirements.txt frontend_req.tmp
RUN pip3 install -r frontend_req.tmp && rm frontend_req.tmp

# Install dependancies and configs.
# requirements.txt most likely to change so put it last
ADD meerkat_dev/frontend/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/frontend/setup_static /usr/bin/setup_static
ADD meerkat_dev/frontend/run /usr/bin/run
WORKDIR /var/www/meerkat_frontend

CMD ["run"]
