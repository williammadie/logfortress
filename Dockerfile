# Use the official Python image.
FROM python:3.13-slim-bookworm AS builder

# Set environment variables to ensure that Python output is sent straight to the terminal (without buffering).
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install uv
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory in the container.
WORKDIR /app

# Copy only the necessary files to install dependencies
COPY pyproject.toml uv.lock /app/

# Copy the pyproject.toml and poetry.lock files to the container.
RUN uv sync --locked

# Copy the rest of the application code to the container.
COPY . /app

# Use a separate stage for the final image
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy only the necessary parts from the builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Expose the port on which the app will run
EXPOSE 2001

# Start the application using uvicorn.
CMD ["uv", "run", "python3", "main.py", "web"]
