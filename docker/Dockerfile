#FROM ubuntu:18.04
FROM tensorflow/tensorflow:2.3.2-gpu

LABEL maintainer "Joao Victor da Fonseca Pinto <jodafons@lps.ufrj.br>"

ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen
USER root
SHELL [ "/bin/bash", "-c" ]


RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone


RUN ls
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    fonts-freefont-otf \
    git \
    wget \
    dpkg-dev \
    g++ \
    gcc \
    binutils \
    xlibmesa-glu-dev \
    libmysqlclient-dev \
    libx11-dev \
    libxpm-dev \
    libxft-dev \
    libxext-dev \
    gfortran \
    libssl-dev \
    libpcre3-dev \
    libglew1.5-dev \
    libftgl-dev \
    libldap2-dev \
    python-dev \
    libxml2-dev \
    libkrb5-dev \
    libgsl0-dev \
    libfftw3-dev \
    libcfitsio-dev \
    graphviz-dev \
    libavahi-compat-libdnssd-dev \
    libboost-all-dev \
    vim \
    librange-v3-dev \
    libboost-python-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Vim tuning
RUN git clone "https://github.com/amix/vimrc.git" "/root/.vim_runtime"
WORKDIR "/root/.vim_runtime/"
RUN source install_awesome_vimrc.sh

# Installing cmake
WORKDIR /usr
RUN wget --progress=dot:giga https://cmake.org/files/v3.19/cmake-3.19.7-Linux-x86_64.sh -P /usr/
RUN chmod 755 /usr/cmake-3.19.7-Linux-x86_64.sh
RUN ./cmake-3.19.7-Linux-x86_64.sh --skip-license
RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN apt-get update && apt-get install -y texlive-full


RUN ls
# Install ROOT
WORKDIR /opt
RUN git clone https://github.com/root-project/root.git
WORKDIR /opt/root
RUN git checkout v6-16-00 && mkdir buildthis 
WORKDIR /opt/root/buildthis
RUN CPU_N=$(grep -c ^processor /proc/cpuinfo) && cmake  --Dpython_version=3 .. && make -j$CPU_N



#RUN wget https://root.cern/download/root_v6.16.00.Linux-ubuntu18-x86_64-gcc7.3.tar.gz
#RUN tar -xzvf root_v6.16.00.Linux-ubuntu18-x86_64-gcc7.3.tar.gz
#RUN source root/bin/thisroot.sh # also available: thisroot.{csh,fish,bat}



RUN ln -sf /usr/bin/pip3 /usr/bin/pip


RUN pip3 install -U pip setuptools

# Install pip packages
RUN pip3 install --no-cache-dir \
    setuptools \
    future \
    tensorflow \
    onnxruntime \
    onnx \
    keras2onnx \
    pandas \
    sklearn \
    seaborn \
    jupyterlab \
    Flask_Security \
    passlib \
    PTable \
    Flask_Mail \
    requests \
    Werkzeug \
    SQLAlchemy \
    Jinja2 \
    Flask \
    Flask_Login \
    Flask_SQLAlchemy \
    BeneDict \
    flask_admin \
    flask_bootstrap \
    flask_cors \
    flask_restful \
    prettytable \
    sqlalchemy_utils \
    psycopg2-binary \
    ansi2html \
    hub \
    pickle5



WORKDIR /
COPY setup_root.sh .
RUN chmod 777 /setup_root.sh
