# Use an official Python runtime as a parent image
FROM python:3.6

# Set the working directory to /app
WORKDIR /alarm_system

# Copy the current directory contents into the container at /app
ADD . /alarm_system

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME Alarm

# Run app.py when the container launches
CMD ["python3", "real_time_object_detection.py"]