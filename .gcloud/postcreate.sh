#!/bin/bash

echo "→ Updating service with service account ${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com"

gcloud run services update $K_SERVICE --platform managed --region ${GOOGLE_CLOUD_REGION} \
    --service-account ${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

# Helpful added message if datastore indexes are still processing
indexes_creating=$(gcloud datastore indexes list --format "value(kind)" --filter "state=CREATING" | wc -l)

SERVICE_URL=$(gcloud run services describe $K_SERVICE --format "value(status.url)" --platform managed --region ${GOOGLE_CLOUD_REGION})

echo "Post-create configuration complete ✨"

echo ""
echo ""
echo "Mewgram is now deployed to ${SERVICE_URL}"
echo ""

if [ $indexes_creating -ne 0 ]; then 
    echo "⚠️  Datastore is still processing, so you may need to wait a few minutes for that to finish."
    echo "   You can check it's ready by checking:"
    echo "gcloud datastore indexes list --format 'value(state, kind)'"
    echo ""
fi

echo "ℹ️  To login into the Django admin: "
echo "  * go to ${SERVICE_URL}/admin"
echo "  * login with the username and password that are stored in Secret Manager"
echo ""
echo "gcloud secrets versions access latest --secret ADMINEMAIL"
echo "gcloud secrets versions access latest --secret ADMINPASS"
echo ""

