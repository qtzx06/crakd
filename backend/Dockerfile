# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
# The source path is now relative to the Dockerfile's location (the 'backend' folder)
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code to the working directory
COPY app/ ./app

# Expose the port the app runs on
EXPOSE 10000

# Define the command to run your app
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "10000"]