# mewgram

*A demo serverless Django micro-blogging app, but it's cats.*

Before deploying: ensure the project you deploy to has [Cloud Firetore in Datastore mode enabled](https://console.cloud.google.com/datastore/setup), and deploy this service to the same region. 

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run)

## local development

1. Copy the `.env_template` file to `.env`, and set the template values. 

1. Set up a Python virtual environment, and install the dependencies: 

    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements
    ```

1. Run the Django migration commands, and start the server: 

    ```
    ./manage.py migrate
    ./manage.py loaddata sampledata
    ./manage.py collectstatic --no-input
    ./manage.py runserver
    ```
