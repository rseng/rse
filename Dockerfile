FROM bitnami/minideb:bookworm

# docker build -t quay.io/vanessa/rse .
LABEL MAINTAINER @vsoch
ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8
ENV RSE_DATABASE sqlite
ENV RSE_HOSTNAME 0.0.0.0
ENV SHELL /bin/bash
RUN /bin/bash -c "install_packages wget bzip2 ca-certificates git && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh"
ADD . /tmp/repo
WORKDIR /tmp/repo
RUN pip install .[all]
ENTRYPOINT ["/opt/conda/bin/rse"]
CMD ["start"]
