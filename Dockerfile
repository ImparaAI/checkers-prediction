FROM debian:stretch-slim

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
	bash \
	python3 \
	python3-pip \
	supervisor

RUN pip3 install -U \
	h5py \
	numpy \
	tensorflow \
	keras \
	flask

COPY docker/conf/supervisord.conf /etc/supervisor.d/supervisord.ini
COPY docker/conf/.bashrc /root/.bashrc
COPY docker/start.sh /bin/original_start.sh

RUN ln -snf /bin/bash /bin/sh && \
    apt-get clean && \
	apt-get autoremove && \
	rm -rf /var/lib/apt/lists/* && \
	rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin && \
	find /usr/lib/python3 -name __pycache__ | xargs rm -r && \
	sed -i -e 's/\r$//' /root/.bashrc && \
    tr -d '\r' < /bin/original_start.sh > /bin/start.sh && \
    chmod -R 700 /bin/start.sh

COPY . /var/app

WORKDIR /var/app

EXPOSE 80

ENV TERM xterm-color
ENV TF_CPP_MIN_LOG_LEVEL 2 #disables cpu compile warnings

CMD ["sh", "/bin/start.sh"]