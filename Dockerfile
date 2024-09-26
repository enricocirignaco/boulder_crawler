# Use Python image
FROM python:3.9-slim

# Install dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libasound2 libwayland-client0 \
    libwayland-cursor0 libwayland-egl1 libxkbcommon0 libgtk-3-0 libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and required Python packages
RUN pip install playwright
RUN playwright install
RUN pip install python-dotenv
# Add the crawler script to the Docker image
COPY script.py /app/script.py
COPY .env /app/.env
# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "script.py"]