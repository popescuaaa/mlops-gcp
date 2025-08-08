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
gcloud run deploy predictor \
  --image="$IMAGE_NAME" \
  --region=europe-west1 \
  --platform=managed \
  --allow-unauthenticated \
  --service-account="$SA" \
  --memory=2Gi \
  --cpu=2 \
  --concurrency=80 \
  --timeout=300s \
  --min-instances=0 \
  --max-instances=10

echo "Deployment complete!"
