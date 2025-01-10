FROM mcr.microsoft.com/dotnet/core/sdk:3.1 AS build-env
WORKDIR /app

# Copy csproj and restore as distinct layers
COPY *.csproj ./
RUN dotnet restore

# Copy everything else and build
COPY . ./
RUN dotnet publish -c Release -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1

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
