# Stage 1: Build Environment (using a slim Python base)
FROM python:3.11-slim as builder

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for building the packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to optimize Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime Environment (smaller image for deployment)
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy runtime dependencies and installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the rest of the application code
COPY app /app/app
# COPY test.db /app/test.db  # Removed because test.db does not exist

# Expose the port Uvicorn runs on
EXPOSE 8000

# Command to run the application (Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
