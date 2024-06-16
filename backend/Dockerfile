# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /api

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port FastAPI is running on
EXPOSE 8085

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085"]
