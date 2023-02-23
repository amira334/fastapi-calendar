FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app directory into the container, excluding the venv directory
COPY . .

# Expose the port that the app will run on
EXPOSE 8000

# Define the command to run the app when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]