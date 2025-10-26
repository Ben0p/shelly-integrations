#######################################
# Built and pushed via Github actions #
#######################################

# Use the official Alpine image as a base
FROM python:alpine

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy src to app
COPY src/ .

# Run the test script
CMD ["python", "main.py", "--env", "docker"]