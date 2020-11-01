# Yahoo Fantasy Football Transaction Email Notification

Uses [YFPY](https://github.com/uberfastman/yfpy), MongoDB, and Heroku's cronjob clock process to email reports when new transactions occurs.

## Setup

Python3 installed

```
venv env
source env/bin/activate
pip install -r requirements.txt
```

Create .env file using the following variables.
```
consumer_key=
consumer_secret=
mongodb=
receiver_email=
sender_email=
sender_password=
league_id=
```

Make sure to authenticate once before deploying clock process following [YFPY](https://github.com/uberfastman/yfpy) guide.
This will add the neccessary token.json file needed to make the requests.

Heroku Deployment

```
heroku create
git push heroku master
heroku ps:scale clock=1
```
