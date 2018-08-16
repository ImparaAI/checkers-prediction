FROM alpine:3.8

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories && \
  apk --no-cache add \
    bash \
    sed \
    git \
    nginx \
    uwsgi \
    uwsgi-python \
    py2-pip \
    supervisor

ENV TERM xterm-color
ENV APP_DIR /app

RUN pip2 install --upgrade pip && \
    pip2 install flask && \
    mkdir ${APP_DIR} && \
    chown -R nginx:nginx ${APP_DIR} && \
    chmod 777 /run/ -R && \
    chmod 777 /root/ -R

COPY docker/conf/supervisord.conf /etc/supervisor.d/supervisord.ini
COPY docker/conf/nginx.conf /etc/nginx/nginx.conf
COPY docker/conf/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY docker/conf/.bashrc /root/.bashrc
COPY docker/start.sh /bin/original_start.sh

RUN ln -snf /bin/bash /bin/sh && \
    sed -i -e 's/\r$//' /root/.bashrc && \
    tr -d '\r' < /bin/original_start.sh > /bin/start.sh && \
    chmod -R 700 /bin/start.sh && \
    rm -fr /var/cache/apk/*

WORKDIR ${APP_DIR}

EXPOSE 80

CMD ["sh", "/bin/start.sh"]