FROM python:3.10.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./backend /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="8000"

# Run app.py when the container launches
CMD ["sh", "-c", "uvicorn ${MODULE_NAME}:${VARIABLE_NAME} --host 0.0.0.0 --port ${PORT}"]
