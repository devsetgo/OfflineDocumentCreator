FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install necessary utilities, dependencies, and wkhtmltopdf
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    wget \
    xfonts-base \
    xfonts-75dpi \
    fontconfig \
    libjpeg62-turbo \
    libxrender1 \
    libxext6 \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || apt-get -f install \
    && rm -rf /var/lib/apt/lists/* \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb

ENV PYTHONUNBUFFERED 1

# [Optional] Uncomment to install additional OS packages or Python requirements
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

