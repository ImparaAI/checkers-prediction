FROM alpine:3.8

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories && \
  apk --no-cache add \
    bash \
    sed \
    git \
    nginx \
    uwsgi-python3 \
    python3 \
    supervisor

ENV TERM xterm-color
ENV APP_DIR /var/app

RUN pip3 install --upgrade pip && \
    mkdir ${APP_DIR}

COPY docker/conf/supervisord.conf /etc/supervisor.d/supervisord.ini
COPY docker/conf/nginx.conf /etc/nginx/nginx.conf
COPY docker/conf/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY docker/conf/.bashrc /root/.bashrc
COPY docker/start.sh /bin/original_start.sh
COPY ./app /var/app

RUN ln -snf /bin/bash /bin/sh && \
    sed -i -e 's/\r$//' /root/.bashrc && \
    tr -d '\r' < /bin/original_start.sh > /bin/start.sh && \
    chmod -R 700 /bin/start.sh && \
    rm -fr /var/cache/apk/* && \
    pip3 install --no-cache-dir -r /var/app/requirements.txt && \
    chown -R nginx:nginx ${APP_DIR}

WORKDIR ${APP_DIR}

EXPOSE 80

CMD ["sh", "/bin/start.sh"]