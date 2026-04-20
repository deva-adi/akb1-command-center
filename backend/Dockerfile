# --- Stage 1: Build ---
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Runtime ---
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code and Alembic assets
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./alembic.ini

# Create non-root user (UID 1001) and writable data dir — SECURITY_GUIDE.md §10
RUN addgroup --system --gid 1001 akb1 \
    && adduser --system --uid 1001 --ingroup akb1 akb1 \
    && mkdir -p /data \
    && chown -R akb1:akb1 /data /app

USER 1001

EXPOSE 9001

# Health check uses Python stdlib so we do not need curl in the image.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001", "--log-level", "info"]
