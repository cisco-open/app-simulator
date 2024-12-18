FROM alpine:3.20.3

LABEL org.opencontainers.image.source=https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="curl loader for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

RUN apk add --no-cache curl util-linux jq
WORKDIR /usr/bin/
COPY entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
