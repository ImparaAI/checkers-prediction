FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && \
	curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
	echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
	echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
	apt-get purge --autoremove -y curl

ENV CUDA_VERSION 10.0.130
ENV CUDA_PKG_VERSION 10-0=$CUDA_VERSION-1
ENV NCCL_VERSION 2.3.5
ENV CUDNN_VERSION 7.3.1.20

RUN apt-get update -y && apt-get upgrade -y && \
	apt-get install -y \
		bash \
		python3 \
		python3-pip \
		default-libmysqlclient-dev \
		cuda-cudart-$CUDA_PKG_VERSION \
		cuda-compat-10-0=410.48-1 \
		cuda-libraries-$CUDA_PKG_VERSION \
		cuda-nvtx-$CUDA_PKG_VERSION \
		libnccl2=$NCCL_VERSION-2+cuda10.0 \
		libcudnn7=$CUDNN_VERSION-1+cuda10.0 && \
	apt-mark hold libnccl2 libcudnn7 && \
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
	mysqlclient \
	imparaai-checkers \
	imparaai-montecarlo

COPY docker/conf/circus.ini /etc/circus/circus.ini
COPY docker/conf/.bashrc /root/.bashrc
COPY docker/start.sh /bin/original_start.sh

RUN ln -snf /bin/bash /bin/sh && \
	ln -s cuda-10.0 /usr/local/cuda && \
	find /usr/lib/python3 -name __pycache__ | xargs rm -r && \
	sed -i -e 's/\r$//' /root/.bashrc && \
	tr -d '\r' < /bin/original_start.sh > /bin/start.sh && \
	chmod -R 700 /bin/start.sh

COPY . /var/app

WORKDIR /var/app

EXPOSE 80

ENV TERM xterm-color
ENV TF_CPP_MIN_LOG_LEVEL 2 #disables cpu compile warnings
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP main.py
ENV PATH /usr/local/cuda/bin:${PATH}
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=10.0 brand=tesla,driver>=384,driver<385"

CMD ["sh", "/bin/start.sh"]