# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run:app
ENV FLASK_ENV=production

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if any (e.g., for psycopg2 if using PostgreSQL)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 5000

# Define the command to run the application using Gunicorn
# The number of workers can be adjusted based on CPU cores, e.g., (2 * CPU_CORES) + 1
# The bind address 0.0.0.0 makes it accessible from outside the container
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "run:app"]
