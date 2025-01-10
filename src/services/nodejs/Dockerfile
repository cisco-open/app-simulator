FROM node:23@sha256:2f73096d856b0b9d6fa43002edb619f1527f939bab870eab6c909f633bcf56e9

LABEL org.opencontainers.image.source=https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="nodejs service for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN chmod +x /app/entrypoint.sh
EXPOSE 80
CMD ["/app/entrypoint.sh"]
