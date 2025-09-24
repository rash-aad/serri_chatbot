# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies using the CPU-only version of PyTorch to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Run the script to build the knowledge base. This happens ONCE during the build.
RUN python setup_knowledge_base.py

# Tell Docker that the container listens on this port
EXPOSE 5001

# The command to run your application when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
