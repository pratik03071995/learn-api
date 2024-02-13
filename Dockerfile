# Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Environment variable to specify the location of the database file within the container
ENV DATABASE=/app/university.db

# Run app.py when the container launches
CMD ["python", "app.py"]
