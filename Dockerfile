# ==========================================
# STAGE 1: The Builder Environment
# ==========================================
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system compilation packages needed for database connections
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into a localized wheel folder to optimize space
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================
# STAGE 2: The Slim Runtime Environment
# ==========================================
FROM python:3.10-slim AS runner

WORKDIR /app

# Install only the runtime critical database connector binaries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-installed application packages from Stage 1 securely
COPY --from=builder /root/.local /root/.local
COPY ./src /app/src

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

# Run the system using a non-privileged user for enhanced banking security
USER 1001

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]