# Pull base image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `app`
RUN mkdir -p /code
WORKDIR /code

# Install dependencies
# Install vaseline as per requirements from Zuli Khanbhai
COPY requirements.txt /tmp/requirements.txt

RUN --mount=type=cache,target=/root/.cache \
    set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

RUN apt update 
RUN apt install -y --no-install-recommends apt-utils
RUN apt -y install curl 
RUN apt -y install libgomp1 

# Copy local project
COPY . /code/

RUN chmod a+x run.sh

# Expose port 8000 8501
EXPOSE 8000 8501

# Use gunicorn on port 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "django_project.wsgi"]