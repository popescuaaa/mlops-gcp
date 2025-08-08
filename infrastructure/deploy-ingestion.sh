#!/bin/bash
set -e

# Get the image name from the first argument
IMAGE_NAME=$1
SA=$2

if [ -z "$IMAGE_NAME" ]; then
  echo "Error: No image name provided"
  exit 1
fi

if [ -z "$SA" ]; then
  echo "Error: No service account provided"
  exit 1
fi

echo "Deploying image: $IMAGE_NAME"

# Deploy to Cloud Run
gcloud run jobs create ingestion \
  --image="$IMAGE_NAME" \
  --region=europe-west1 \
  --service-account="$SA" \
  --memory=2Gi \
  --cpu=2 \
  --timeout=30m \
  --max-retries=3 \
  --task-timeout=30m

echo "Deployment complete!"
