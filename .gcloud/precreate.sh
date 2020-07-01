#!/bin/bash

time source waitforindexes.sh

echo "🚀 Running initial Django migration (this will take a few minutes)..."
echo "   Configurations: service ${K_SERVICE}, region ${GOOGLE_CLOUD_REGION}"

gcloud builds submit --config .gcloud/cloudbuild.yaml

if [ $? -ne 0 ]; then
    echo "❌ Cloud Build failed. Check logs."
else
    echo "Pre-create data migration complete ✨"
fi
