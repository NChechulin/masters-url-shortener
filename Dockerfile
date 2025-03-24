# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Run migrations then start the FastAPI application.
# The 'sh -c' command runs the alembic migration before starting uvicorn.
CMD sh -c "sleep 5 && alembic upgrade head && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
