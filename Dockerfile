# Use an official Python runtime as a parent image
FROM python:3.12.0

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Pipenv
RUN pip install pipenv

# Install any needed packages specified in requirements.txt
RUN pipenv install --deploy --ignore-pipfile

# Expose the port that Gunicorn will run on
EXPOSE 8080

# Run the Flask application using Gunicorn
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
