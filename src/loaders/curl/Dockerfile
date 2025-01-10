FROM alpine:3.21.2@sha256:56fa17d2a7e7f168a043a2712e63aed1f8543aeafdcee47c58dcffe38ed51099

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
