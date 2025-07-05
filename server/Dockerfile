# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg unzip curl --fix-missing && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*


# Install a fixed version of ChromeDriver compatible with Chrome 114
ENV CHROMEDRIVER_VERSION 114.0.5735.90
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create output directories
RUN mkdir -p data_output/raw data_output/processed data_output/reports

# Clean webdriver-manager cache to avoid ChromeDriver exec format errors
RUN rm -rf /root/.wdm

# Entrypoint defaults to bash shell
ENTRYPOINT ["uvicorn", "src.api.v1:app", "--host", "0.0.0.0", "--port", "8000"]
