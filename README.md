# Yahoo Fantasy Football Transaction Email Notification

Uses [YFPY](https://github.com/uberfastman/yfpy), MongoDB, and Heroku's cronjob clock process to email reports when new transactions occurs.

## Setup

Make sure Python3 is installed.

Create a virtual environment and install the dependencies.
```
venv env
source env/bin/activate
pip install -r requirements.txt
```

Create an `.env` file using the following variables.

```
consumer_key=
consumer_secret=
mongodb=
receiver_email=
sender_email=
sender_password=
league_id=
```

You will need to register your app at [Yahoo Developer](https://developer.yahoo.com/apps/create/) to obtain a `consumer_key` and `consumer_secret`.

You will also need a MongoDB database connection string. Sign up at [MongoDB](https://www.mongodb.com/) to setup a free cluster.


## Heroku Deployment

Before deploying you will need to manually authenticate the app with Yahoo. This will generate a `token.json` file required to make requests.

Create a Heroku app and a clock process. By default the job will run every 30 seconds and can be configured in `job.py`.

```
heroku create
git push heroku master
heroku ps:scale clock=1
heroku logs --tail
```
