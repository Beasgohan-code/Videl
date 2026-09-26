FROM python:3.10-slim

# System deps: ffmpeg is required for audio/video; curl/git for installs
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ffmpeg \
        unzip \
        curl \
        wget \
        git \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://deno.land/install.sh | sh

ENV DENO_INSTALL="/root/.deno"
ENV PATH="${DENO_INSTALL}/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./

# Install deps, then FORCE latest yt-dlp (YouTube extractors change often)
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir --prefer-binary -r requirements.txt && \
    python -m pip install --no-cache-dir -U "yt-dlp[default]" && \
    yt-dlp --version && \
    ffmpeg -version | head -1

COPY . .

# Make entrypoint executable
RUN chmod +x /app/start || true

EXPOSE 10000

# Upgrade yt-dlp on every container start, then run bot
CMD ["bash", "-c", "python -m pip install -U --quiet yt-dlp 2>/dev/null || true; exec python main.py"]
