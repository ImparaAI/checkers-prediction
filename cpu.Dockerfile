FROM debian:stretch-slim

RUN apt-get update -y && apt-get upgrade -y && \
	apt-get install -y \
		bash \
		cron \
		python3 \
		python3-pip \
		sqlite && \
	apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/* && \
	rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin

RUN pip3 install -U \
	setuptools \
	h5py \
	numpy \
	circus \
	chaussette \
	tensorflow \
	keras \
	flask \
	pytest \
	imparaai-checkers \
	imparaai-montecarlo

COPY docker/conf/circus.ini /etc/circus/circus.ini
COPY docker/conf/.bashrc /root/.bashrc
COPY docker/start.sh /bin/original_start.sh
COPY docker/crontab /var/cron

RUN ln -snf /bin/bash /bin/sh && \
	find /usr/lib/python3 -name __pycache__ | xargs rm -r && \
	sed -i -e 's/\r$//' /root/.bashrc && \
    tr -d '\r' < /bin/original_start.sh > /bin/start.sh && \
    chmod -R 700 /bin/start.sh && \
	sed -i -e 's/\r$//' /var/cron && \
    chmod 0755 /var/cron && \
    /usr/bin/crontab /var/cron

COPY . /var/app

WORKDIR /var/app

EXPOSE 80

ENV TERM xterm-color
ENV TF_CPP_MIN_LOG_LEVEL 2 #disables cpu compile warnings
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP main.py

CMD ["sh", "/bin/start.sh"]