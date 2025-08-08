#!/bin/bash

# Set variables
PROJECT_ID=$(gcloud config get-value project)
LOCATION="europe-west1"  # Change as needed
REPOSITORY_NAME=""
DESCRIPTION="Docker container repository for $REPOSITORY_NAME"

# Create the Artifact Registry repository
gcloud artifacts repositories create $REPOSITORY_NAME \
    --repository-format=docker \
    --location=$LOCATION \
    --description="$DESCRIPTION" \
    --project=$PROJECT_ID

# Configure Docker to use the repository
# gcloud auth configure-docker $LOCATION-docker.pkg.dev

echo "Docker repository created: $LOCATION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME"
