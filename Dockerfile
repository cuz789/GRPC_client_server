# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables for Redis connection (Optional, if using environment variables)
# ENV REDIS_HOST=your_redis_host
# ENV REDIS_PORT=your_redis_port
# ENV REDIS_USERNAME=your_redis_username
# ENV REDIS_PASSWORD=your_redis_password

# Make port 50051 available to the world outside this container
EXPOSE 50051

# Run server.py when the container launches
CMD ["python", "server.py"]
