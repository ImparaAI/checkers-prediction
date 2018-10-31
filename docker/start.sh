#!/bin/bash

cd /var/app

if [ "$USE_GPU" != "true" ]; then
	export CUDA_VISIBLE_DEVICES="-1"
	export CUDA_DEVICE_ORDER="PCI_BUS_ID"
fi

echo "Attempting to initialize the database..."

until flask database:initialize >/dev/null 2>/dev/null
do
	echo "Database initialization failed, retrying until success..."
done

echo "Database initialized"

touch /var/healthy

circusd /etc/circus/circus.ini