FROM debian:stable
MAINTAINER Silvio Rhatto <rhatto@torproject.org>

ENV APP="onionprobe"
ENV APP_BASE="/srv/"
ENV SHELL="/bin/bash"
ENV ONIONPROBE_CONFIG="/srv/onionprobe/configs/tor.yaml"

RUN apt-get update && \
    apt-get install -y \
    python3-prometheus-client python3-stem python3-cryptography \
    python3-bs4 python3-yaml python3-pytest python3-requests \
    python3-socks tor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_BASE}/${APP}

COPY . ${APP_BASE}/${APP}

USER debian-tor

ENTRYPOINT exec /srv/onionprobe/onionprobe -c ${ONIONPROBE_CONFIG}
