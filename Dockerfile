# Use the official Python image from the Docker Hub, adapted to the project's needs
FROM python:3.10.16-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# [alternative] Copy the required directories only into the container. For example:
# COPY app/ app/
# COPY deep_learning_model/ deep_learning_model/

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
