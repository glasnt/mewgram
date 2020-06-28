# mewgram

*A demo Django micro-blogging app, but it's cats.*

TODO(glasnt): implement custom Cloud Run Button functions

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
