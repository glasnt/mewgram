# mewgram

*A demo Django micro-blogging app, but it's cats.*

Before deploying: ensure the project you deploy to has [Cloud Firetore in Datastore mode enabled](https://console.cloud.google.com/datastore/setup)

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

## local development

1. Run [`robocat`](https://github.com/glasnt/robocat) in another terminal.

1. Copy the `.env_template` file to `.env`, and set the template values. 

1. Run this Django server:

    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements
    ./manage.py migrate
    ./manage.py runserver
    ```
