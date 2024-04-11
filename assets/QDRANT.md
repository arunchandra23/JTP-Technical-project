# Running Qdrant Docker Image & Taking a Snapshot of the Collection

## Overview

This guide provides detailed instructions on how to set up and run the Qdrant Docker image for managing vector databases and how to take a snapshot of a collection directly from the Qdrant dashboard. Qdrant is a vector search engine that enables efficient similarity search for high-dimensional data, such as image feature vectors, making it ideal for applications like image recommendation systems.

## Running Qdrant with Docker

### Prerequisites

- Docker installed on your machine.
- Basic understanding of Docker and terminal commands.

### Steps to Run Qdrant Docker Image

1. **Pull the Qdrant Docker Image:**
   Open your terminal and pull the latest Qdrant image from Docker Hub by running:
   ```bash
   docker pull qdrant/qdrant
   ```
   
2. **Run the Qdrant Container:**
   After pulling the image, run the container using the following command. This command also maps the Qdrant default port (`6333`) from the container to your host, making the Qdrant dashboard accessible via your web browser.
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
   Now, Qdrant is running on your machine, and you can access the dashboard through [http://localhost:6333/dashboard](http://localhost:6333/dashboard).

## Taking a Snapshot from the Qdrant Dashboard

### Prerequisites

- Running Qdrant instance.
- Existing data collection in Qdrant.

### Steps to Take a Snapshot

1. **Access the Dashboard:**
   Open a web browser and navigate to the Qdrant dashboard at [http://localhost:6333/dashboard](http://localhost:6333/dashboard).

2. **Navigate to the Collections Tab:**
   In the dashboard's sidebar, click on the "Collections" tab to view the list of existing collections in your Qdrant instance.

3. **Select Your Collection:**
   From the list of collections, click on the collection for which you want to take a snapshot.

4. **Take a Snapshot:**
   Inside the collection's details page, look for the "Snapshot" section or a button labeled "Take Snapshot". Clicking this will initiate the process to create a snapshot of the current state of your collection.

5. **Monitor the Snapshot Process:**
   The dashboard may provide feedback on the progress of the snapshot process. Wait for the process to complete successfully.

6. **Accessing the Snapshot:**
   Once the snapshot is complete, the dashboard will usually provide details on where the snapshot has been saved. This typically includes the snapshot's filename and its location on the server running Qdrant.

> **Note:** The exact steps and labels might vary slightly depending on the version of the Qdrant dashboard you are using. If you encounter any discrepancies, refer to the official [Qdrant documentation](https://qdrant.tech/documentation/) for the most accurate and up-to-date information.

This guide should help you get started with running Qdrant in a Docker container and taking snapshots of your collections from the Qdrant dashboard.