FROM alpine:3.20.3
RUN apk add --no-cache curl=8.11.0-r2 util-linux=2.40.1-r1
WORKDIR /usr/bin/
COPY loader.sh /usr/bin
RUN chmod +x /usr/bin/loader.sh
ENTRYPOINT ["/usr/bin/loader.sh"]
