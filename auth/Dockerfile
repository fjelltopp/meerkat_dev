FROM python:3.7

RUN apt-get update
# Install global requirements
    apt-get install -y nodejs gettext &&\
    apt-get clean &&\
    npm install -g bower gulp yarn &&\

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
