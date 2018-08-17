#!/bin/bash

touch /var/healthy

supervisord -c /etc/supervisor.d/supervisord.ini