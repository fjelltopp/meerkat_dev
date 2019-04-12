FROM python:3.6.2
RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update
# Install global requirements
ENV PYTHONPATH=/var/www/meerkat_libs
RUN wget -qO- https://deb.nodesource.com/setup_10.x | sed 's/apt-get update/apt-get -o Acquire::Check-Valid-Until=false update/' | bash - &&\
    apt-get install -y nodejs gettext ghostscript &&\
    apt-get clean &&\
    pip3 install uwsgi
RUN npm install -g bower gulp-cli yarn
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
