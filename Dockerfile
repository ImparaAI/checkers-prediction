FROM petronetto/docker-python-deep-learning

RUN apt-get update && \
    apt-get install -y \
      supervisor

RUN ln -snf /bin/bash /bin/sh && \
    rm -fr /var/cache/apk/* && \
    pip3 install flask

COPY docker/conf/supervisord.conf /etc/supervisor.d/supervisord.ini
COPY docker/conf/.bashrc /root/.bashrc
COPY docker/start.sh /bin/original_start.sh

RUN sed -i -e 's/\r$//' /root/.bashrc && \
    tr -d '\r' < /bin/original_start.sh > /bin/start.sh && \
    chmod -R 700 /bin/start.sh && \
    rm /usr/bin/python && \
    ln -s /usr/bin/python3 /usr/bin/python

COPY . /var/app

WORKDIR /var/app

EXPOSE 80

ENV TERM xterm-color

CMD ["sh", "/bin/start.sh"]