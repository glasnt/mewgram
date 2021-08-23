# mewgram

*This is a demo of a Django app using Google Datastore via [django-gcloud-connectors](https://gitlab.com/potato-oss/google-cloud/django-gcloud-connectors). Read the [dev.to post](https://dev.to/googlecloud/pure-serverless-django-with-django-gcloud-connectors-apo)*.

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

🚨 **Before deploying**: ensure the project you deploy to has [Cloud Firestore in Datastore mode enabled](https://console.cloud.google.com/datastore/setup), and deploy this service to the same region. 


## local development (in sqlite)

1. Copy the `.env_template` file to `.env`, and set the template values. 

1. Set up a Python virtual environment, and install the dependencies: 

    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

1. Run the Django migration commands, and start the server: 

    ```
    ./manage.py migrate
    ./manage.py loaddata sampledata
    ./manage.py collectstatic --no-input
    ./manage.py runserver
    ```

## datastore configurations of note: 

To use the datastore backend: 

 * add `django-gcloud-connectors` to [`requirements.txt`](requirements.txt),
 * add `gcloudc` to the top of `INSTALLED_APPS` in [`settings.py`](settings.py), 
 * add `gcloudc.db.backends.datastore` as an `ENGINE` in `DATABASES` in `settings.py`.

When testing your app, set `DEBUG=True` in your `settings.py` or `.env`, and when encountering `400 no matching index found` errors: 

 * append the recommended index to `index.yaml`,
 * run `gcloud datastore indexes create index.yaml`,
 * wait for the index(es) to be ready: 

    ```
    gcloud datastore indexes list --format "value(state,kind)"
    ```

For more details, see the [django-gcloud-connectors project docs](https://gitlab.com/potato-oss/google-cloud/django-gcloud-connectors).

## other google cloud configurations of note

This project additionally makes use of: 

 * Google Secret Manager, 
 * Google Cloud Build,
 * Google Cloud Storages (via `django-storages[google]`), and
 * Google Cloud Run. 

Deployment details can be found in `.gcloud/`, and more details about the Django-specific use of the Google components can be found in the [`django-demo-app-unicodex` docs](https://github.com/GoogleCloudPlatform/django-demo-app-unicodex/tree/master/docs).

## cats

mewgram uses [Robohash](https://github.com/e1ven/Robohash) set #4 for it's identicons. Robohash is available as a [Python package](https://pypi.org/project/robohash/). 

## limitations

While this app does use Datastore, the major limitation it faces is due to [indexes](https://cloud.google.com/appengine/docs/flexible/java/configuring-datastore-indexes-with-index-yaml). 

The indexes defined in `index.yaml` is sufficient to navigate the entire app front end, and base admin pages, but _not_ for: 

 * sorting in the admin,
 * running Hypothesis tests. 
