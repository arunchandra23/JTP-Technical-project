# Use the official Node.js 16 image as the base image for the build stage
FROM node:16 as build-stage

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the package.json and package-lock.json files from the local machine to the container's /app directory
COPY ./frontend/package*.json /app/

# Install the serve package globally using npm
RUN npm install serve -g

# Install the dependencies specified in the package.json file
RUN npm install

# Copy all the files from the local machine's frontend directory to the container's /app directory
COPY ./frontend/ /app/

# Build the frontend application
RUN npm run build

# Expose port 3003 to allow incoming connections
EXPOSE 3003

# Start the frontend application using the serve command
CMD ["npm", "run", "serve"]
