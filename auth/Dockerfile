FROM python:3.6.2

RUN echo "deb [check-valid-until=no] http://archive.debian.org/debian jessie-backports main" > /etc/apt/sources.list.d/jessie-backports.list

RUN sed -i '/deb http:\/\/deb.debian.org\/debian jessie-updates main/d' /etc/apt/sources.list

RUN apt-get -o Acquire::Check-Valid-Until=false update
# Install global requirements
RUN wget -qO- https://deb.nodesource.com/setup_10.x | sed 's/apt-get update/apt-get -o Acquire::Check-Valid-Until=false update/' | bash - &&\
    apt-get install -y nodejs gettext &&\
    apt-get clean &&\
    npm install -g bower gulp yarn &&\
    pip3 install uwsgi

WORKDIR /var/www/
ADD meerkat_libs/requirements.txt libs_req.tmp
RUN pip3 install -r libs_req.tmp
ADD meerkat_auth/requirements.txt auth_req.tmp
RUN pip3 install -r auth_req.tmp &&\
    rm *_req.tmp

WORKDIR /var/www/meerkat_auth
ENV PYTHONPATH=/var/www/meerkat_libs:/var/www/meerkat_auth
ADD meerkat_dev/auth/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/auth/setup_static /usr/bin/setup_static
ADD meerkat_dev/auth/run /usr/bin/run

CMD ["run"]
