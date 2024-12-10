FROM alpine:3.20.3
RUN apk add --no-cache curl util-linux
WORKDIR /usr/bin/
COPY loader.sh /usr/bin
RUN chmod +x /usr/bin/loader.sh
ENTRYPOINT ["/usr/bin/loader.sh"]
