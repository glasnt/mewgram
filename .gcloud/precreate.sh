#!/bin/bash
echo "ℹ️  Waiting for Datastore indexes to be ready"

function get_indexes { 
    state=$(gcloud datastore indexes list --format "value(state,kind)")
    ready=$(echo $state | grep "READY" | wc -l)
    creating=$(echo $state | grep "CREATING" | wc -l)
} 
START=$(date +%s.%N)
get_indexes

if [ $creating -ne 0 ]; then echo "Waiting for indexes to be ready"; fi

while [ $creating -ne 0 ]
do
    echo "... $creating creating, $ready ready ..."
    sleep 5
    get_indexes
done

END=$(date +%s.%N)
echo "... Indexes ready (waited $(echo "$END - $START" | bc | cut -d'.' -f1)s."
echo $state

echo "🚀 Running initial Django migration (this will take a few minutes)..."
echo "   Configurations: service ${K_SERVICE}, region ${GOOGLE_CLOUD_REGION}"

gcloud builds submit --config .gcloud/cloudbuild.yaml

echo "Pre-create data migration complete ✨"
