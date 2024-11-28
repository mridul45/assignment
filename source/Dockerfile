# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from the requirements file
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=source.settings

# Expose the port Django will run on
EXPOSE 8000

# Collect static files for production (optional, if you're running in production)
# RUN python manage.py collectstatic --noinput

# Run Django migrations
RUN python manage.py migrate

# Start the Django development server (you can change this command for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
