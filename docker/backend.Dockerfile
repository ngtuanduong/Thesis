FROM node:20-slim

# Install system dependencies and Docker CLI from Docker's official repository
# The Debian 'docker.io' package ships Docker 20.10.x (API v1.41) which is
# incompatible with modern Docker Desktop daemons (minimum API v1.44).
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
      openssl procps ca-certificates curl gnupg && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends docker-ce-cli docker-buildx-plugin && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
