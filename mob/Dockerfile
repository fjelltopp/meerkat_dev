FROM python:3.7

RUN apt-get update
# Install global requirements

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

# A note: cryptography might be failing for some reason. 
WORKDIR /var/www/meerkat_mob
ADD meerkat_mob/requirements.txt mob_req.tmp
RUN pip install -r mob_req.tmp && rm mob_req.tmp

ADD meerkat_dev/mob/uwsgi/app.ini /var/www/uwsgi/app.ini
ADD meerkat_dev/mob/run /usr/bin/run

CMD ["run"]
