FROM alpine:3.20.3

LABEL org.opencontainers.image.source https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="curl loader for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

RUN apk add --no-cache curl=8.11.0-r2 util-linux=2.40.1-r1
WORKDIR /usr/bin/
COPY loader.sh /usr/bin
RUN chmod +x /usr/bin/loader.sh
ENTRYPOINT ["/usr/bin/loader.sh"]
