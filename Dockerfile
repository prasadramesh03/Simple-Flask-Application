# Build Stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements first to leverage cache
COPY app/requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ . 

# Final Stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Copy the app from the builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Expose port
EXPOSE 5000

# Switch to non-root user
USER appuser

# Command to run the app
CMD ["python", "app.py"]
