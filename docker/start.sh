#!/bin/bash

cd /var/app

echo "Attempting to initialize the database..."

until flask database:initialize >/dev/null 2>/dev/null
do
	echo "Database initialization failed, retrying until success..."
done

echo "Database initialized"

echo "Starting cron"
cron
echo "Cron started"

touch /var/healthy

circusd /etc/circus/circus.ini

echo "Container started"