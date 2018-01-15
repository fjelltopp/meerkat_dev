FROM python:3.6.2

RUN apt-get update &&\
    pip3 install uwsgi

WORKDIR /var/www/meerkat_mob
ADD meerkat_mob/requirements.txt mob_req.tmp
RUN pip3 install -r mob_req.tmp && rm mob_req.tmp

ADD meerkat_dev/mob/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/mob/run /usr/bin/run

CMD ["run"]
