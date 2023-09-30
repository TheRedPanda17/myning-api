# Use an official Python runtime as a parent image
FROM python:3.10.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages
RUN python setup.py develop

# Make port 8080 available to the world outside this container
EXPOSE 8080