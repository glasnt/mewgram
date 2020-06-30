#!/bin/bash
# migrate
echo "🚀 Running initial Django migration (this will take a few minutes)..."
echo "   Configurations: service ${K_SERVICE}, region ${GOOGLE_CLOUD_REGION}"

gcloud builds submit

gcloud datastore indexes create index.yaml -q

echo "Pre-create data migration complete ✨"
