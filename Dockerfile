FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN set -e && \
    uv venv -p 3.13 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        gnupg \
        unzip \
        curl \
        ca-certificates \
        gawk && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    echo "Detected Chrome version: $CHROME_VERSION" && \
    wget -q https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip -q chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    echo "Chrome version: $(google-chrome --version)" && \
    echo "ChromeDriver version: $(chromedriver --version)" && \
    apt-get purge -y wget gnupg unzip curl gawk && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* chromedriver-linux64*

WORKDIR /app
RUN uv venv -p 3.13
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml .
RUN uv pip install -e ".[cli]" && \
    uv pip compile pyproject.toml --extra firebase

COPY prefect.toml .
COPY src src
RUN chmod -R 755 /app/src/crawler_kit/infrastructure/plugins/chrome/