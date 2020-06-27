# Use Python 3.8
FROM python:3.8

# Prevent Docker from outputting to stdout
ENV PYTHONBUFFERED 1

# Make a directory called "code" which will contain the source code. This will be used as a volume in our docker-compose.yml file
RUN mkdir /code

# Add the contents of the django_events directory to the code directory
ADD ./django_events /code

# Set the working directory for the container. I.e. all commands will be based out of this directory
WORKDIR /code

# Install all dependencies required for this project.
RUN pip install --trusted-host pypy.org --trusted-host files.pythonhosted.org -r requirements.txt