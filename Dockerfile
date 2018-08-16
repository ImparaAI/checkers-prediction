FROM alpine:3.8

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories && \
  apk --no-cache add \
    bash \
    git \
    nginx \
    uwsgi \
    uwsgi-python \
    py2-pip

ENV TERM xterm-color
ENV APP_DIR /app

RUN pip2 install --upgrade pip && \
    pip2 install flask && \
    mkdir ${APP_DIR} && \
    chown -R nginx:nginx ${APP_DIR} && \
    chmod 777 /run/ -R && \
    chmod 777 /root/ -R

COPY conf/docker/nginx.conf /etc/nginx/nginx.conf
COPY conf/docker/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY docker/start.sh /start.sh
COPY docker/start.sh /bin/original_start.sh

WORKDIR ${APP_DIR}

EXPOSE 80

CMD ["sh", "/bin/start.sh"]