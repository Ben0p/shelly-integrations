# Use the official Alpine image as a base
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the test.py file into the container
COPY test.py .

# Run the test script
CMD ["python", "test.py"]

# docker build -t ben0p/shelly-api-collector:20250109.0 .
# docker push ben0p/shelly-api-collector:20250109.0