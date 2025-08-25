# ARG PYTHON_VERSION=3.12.4
# FROM python:${PYTHON_VERSION}-slim AS base

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV FLASK_DEBUG=1

# WORKDIR /app

# # Copy requirements and install dependencies BEFORE switching user.
# COPY requirements.txt .
# RUN --mount=type=cache,target=/root/.cache/pip \
#     python -m pip install -r requirements.txt

# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# # Copy application files AFTER installing dependencies, but BEFORE switching user.
# COPY . .

# USER appuser

# EXPOSE 8000

# # More explicit Gunicorn configuration:
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "gthread", "main:app"]

# # Health check
# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#     CMD curl --fail http://0.0.0.0:8000/ || exit 1


FROM python:3.12.4-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"]