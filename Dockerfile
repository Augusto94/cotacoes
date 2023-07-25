# Use a Python base image
FROM python:3.11

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy only the requirements files first to leverage Docker caching
COPY poetry.lock pyproject.toml /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy the rest of the application code
COPY . /app/

EXPOSE 8000

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
