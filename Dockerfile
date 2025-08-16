FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN set -e \
    && apt-get update \
    && apt-get install -y wget gnupg unzip curl sudo ca-certificates \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip \
    && unzip -qo chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && echo "Chrome version: $(google-chrome --version)" \
    && echo "ChromeDriver version: $(chromedriver --version)"

WORKDIR /app
RUN uv venv -p 3.13
ENV PATH="/app/.venv/bin:$PATH"

ADD pyproject.toml pyproject.toml
RUN uv pip install -e ".[cli]"
RUN uv pip compile pyproject.toml --extra firebase
# RUN uv sync

ADD prefect.toml prefect.toml 
ADD src src
RUN chmod -R 755 /app/src/crawler_kit/infrastructure/plugins/chrome/