FROM python:3.9-slim

WORKDIR /app

# 1. Package lists refresh karo aur vulnerable packages ko explicitly update karo
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends imagemagick gnupg gpg && \
    rm -rf /var/lib/apt/lists/*

# 2. App files copy karo
COPY . .

# 3. bina faaltu cache banaye requirements install karo
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
