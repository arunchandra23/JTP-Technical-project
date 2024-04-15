# Use the Python 3.10.8 base image
FROM python:3.10.8

# Set the working directory inside the container
WORKDIR /app

# Copy the backend directory to the working directory
COPY ./backend /app

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8008 for the container
EXPOSE 8008

# Set environment variables for the module name, variable name, and port
ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="8008"

# Start the application using uvicorn
CMD ["sh", "-c", "uvicorn ${MODULE_NAME}:${VARIABLE_NAME} --host 0.0.0.0 --port ${PORT}"]
