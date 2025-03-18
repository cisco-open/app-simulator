FROM mcr.microsoft.com/dotnet/core/sdk:3.1@sha256:150d074697d1cda38a0c2185fe43895d84b5745841e9d15c5adba29604a6e4cb AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1@sha256:e3b773f30a0a6e88d71ce52429f6847627fc9353e491346902ca345760b82bdd

LABEL org.opencontainers.image.source=https://github.com/cisco-open/app-simulator
LABEL org.opencontainers.image.description="dotnetcore service for app-simulator"
LABEL org.opencontainers.image.licenses=BSD-3-Clause

RUN apt-get update && apt-get install -y \
  unzip \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=build-env /app/out .
COPY entrypoint.sh /app
CMD ["/app/entrypoint.sh"]
