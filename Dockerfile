# Use an official Python runtime as a parent image
FROM python:3.13

# Set the working directory to /app
WORKDIR /celebsite

# Copy the current directory contents into the container at /app
COPY . /celebsite

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable/ change to app
ENV DJANGO_SETTINGS_MODULE=celebsite.settings

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]