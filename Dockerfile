FROM python:3.9-slim

WORKDIR /app

# Install poetry
RUN pip install poetry==1.5.1

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not use virtualenv
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command is specified in docker-compose.yml for each service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]