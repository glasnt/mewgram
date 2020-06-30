#!/bin/bash

echo "→ Updating service with service account"
echo "  ${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com"

gcloud run services update $K_SERVICE --platform managed --region ${GOOGLE_CLOUD_REGION} \
    --service-account ${K_SERVICE}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

echo "Post-create configuration complete ✨"

echo ""
echo ""
echo "Mewgram is now deployed to ${SERVICE_URL}"
echo ""
echo "To login into the Django admin: "
echo "  * go to ${SERVICE_URL}/admin"
echo "  * login with the username and password that are stored in Secret Manager"
echo ""
echo "gcloud secrets versions access latest --secret ADMINEMAIL"
echo "gcloud secrets versions access latest --secret ADMINPASS"
echo ""
