FROM python:3.12-slim

RUN useradd -m -s /bin/bash sandbox

RUN pip install --no-cache-dir numpy

WORKDIR /sandbox

USER sandbox

# Resource limits are applied via Docker run flags:
# --memory=256m --cpus=0.5 --network=none --read-only
CMD ["python3"]
