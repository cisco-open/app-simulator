# There is no arm64 version of mysql:5.7, so we use the amd64 version, until we migrate to mariadb.
# hadolint ignore=DL3029
FROM --platform=linux/amd64 mysql:9.1@sha256:0255b469f0135a0236d672d60e3154ae2f4538b146744966d96440318cc822c6

LABEL org.opencontainers.image.source=https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="mysql database for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

RUN yum install -y php-cli && yum clean all

COPY setup.php /tmp/
COPY setup.sh /docker-entrypoint-initdb.d/
