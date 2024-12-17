FROM node:18

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
