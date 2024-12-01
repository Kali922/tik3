# Use the official Python image
FROM python:3.9-slim

# Set environment variables
#ENV PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose a port if needed (optional)
# EXPOSE 8000

# Set the default command to run the script
CMD ["python3", "run.py"]
