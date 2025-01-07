FROM alpine:3.20.3

LABEL org.opencontainers.image.source=https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="curl loader for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

# Pining versions with alpine regularly breaks, disable linting for this line
# until a better solution is found.
# hadolint ignore=DL3018
RUN apk add --no-cache bash curl util-linux jq
WORKDIR /usr/bin
COPY entrypoint.sh /usr/bin/entrypoint.sh
RUN chmod +x /usr/bin//entrypoint.sh
ENTRYPOINT ["/usr/bin/entrypoint.sh"]
