#!/bin/bash

touch /var/healthy

cd /var/app

echo "Attempting to initialize the database..."

until flask database:initialize
do
	echo "Database initialization failed, retrying until success..."
done

circusd /etc/circus/circus.ini