#!/bin/bash
# migrate
echo "🚀 Running initial Django migration (this will take a few minutes)..."
echo "   Configurations: service ${K_SERVICE}, region ${GOOGLE_CLOUD_REGION}"

gcloud datastore indexes create index.yaml -q
gcloud builds submit

echo "Pre-create data migration complete ✨"
