# Use the latest stable Python runtime as a parent image
FROM python:3.13-slim

ADD . /app

# Set working directory in the container
WORKDIR /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application
CMD ["python", "-u", "main.py"]