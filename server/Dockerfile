# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Chrome
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create output directories
RUN mkdir -p data_output/raw data_output/processed data_output/reports

# Clean webdriver-manager cache to avoid ChromeDriver exec format errors
RUN rm -rf /root/.wdm

# Expose port
EXPOSE 8000

# Entrypoint defaults to uvicorn without reload
ENTRYPOINT ["uvicorn", "src.api.v1:app", "--host", "0.0.0.0", "--port", "8000"]
