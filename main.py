import os, smtplib, ssl
from datetime import datetime
from pymongo import DESCENDING
from yfpy.query import YahooFantasySportsQuery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import DB
from dotenv import load_dotenv
load_dotenv()

db = DB()
client = db.client.prod

def poll_transactions():
    transactions = fetch_transactions()

    if transactions:
        last_transaction = transactions[0]
        last_record_id = 0

        if client.transactions.count() > 0:
            last_record = client.transactions.find().sort('transaction_id', DESCENDING).next()
            last_record_id = int(last_record['transaction_id'])

        number_of_new_transactions = int(last_transaction['transaction'].transaction_id) - last_record_id

        if number_of_new_transactions > 0:
            email_transaction_report(transactions=transactions[0:number_of_new_transactions])
            update_db(transaction_record_obj(last_transaction['transaction']))

def transaction_record_obj(transaction):
    if transaction:
        return {
            "status": transaction.status,
            "timestamp": transaction.timestamp,
            "transaction_id": transaction.transaction_id,
            "transaction_key": transaction.transaction_key,
            "type": transaction.type
        }
    return None

def update_db(transaction_obj):
    if transaction_obj:
        client.transactions.insert_one(transaction_obj)
    return None

def fetch_transactions():
    yahoo_fantasy_sports_query = YahooFantasySportsQuery(".", os.getenv('league_id'), consumer_key=os.getenv('consumer_key'), consumer_secret=os.getenv('consumer_secret'))
    return yahoo_fantasy_sports_query.get_league_transactions()

def email_transaction_report(transactions=[]):
    sender_email = os.getenv('sender_email')
    sender_password = os.getenv('sender_password')
    receiver_email = os.getenv('receiver_email')

    message = MIMEMultipart("alternative")
    message["Subject"] = "New Transaction(s) in your Yahoo Fantasy Football League"
    message["From"] = sender_email
    message["To"] = receiver_email

    plain_body = MIMEText("""New Transaction occured in your Fantasy Football League.""", "plain")
    html_body = MIMEText(transaction_html_summary(transactions=transactions), "html")

    message.attach(plain_body)
    message.attach(html_body)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def transaction_html_summary(transactions=[]):
    html = """<html><body><h2>""" + str(len(transactions)) + """ new transaction(s)</h2>"""
    for transaction in transactions:
        transaction_obj = transaction['transaction']
        if transaction_obj.type in ("add", "drop"):
            html += single_player_transaction_html(transaction_obj)
        if transaction_obj.type == "add/drop":
            html += multiple_player_transaction_html(transaction_obj)
    html += """</body></html>"""
    return html

def single_player_transaction_html(transaction_obj=None):
    if transaction_obj is None:
        return ""

    html = """<table style="border: 0.5px solid black">"""
    time_display = datetime.fromtimestamp(int(transaction_obj.timestamp)).strftime("%b %d %Y %-I:%M %p")
    player_obj = transaction_obj.players['player']
    team_name = player_obj.transaction_data.destination_team_name if transaction_obj.type == "add" else player_obj.transaction_data.source_team_name

    html += """<thead><tr><th colspan="2">%s - %s</th></tr></thead>""" % (team_name, time_display)
    html += player_table_row_html(player_obj)
    html += """</tr></table><br />"""
    return html

def multiple_player_transaction_html(transaction_obj=None):
    if transaction_obj is None:
        return ""

    html = """<table style="border: 0.5px solid black">"""
    time_display = datetime.fromtimestamp(int(transaction_obj.timestamp)).strftime("%b %d %Y %-I:%M %p")
    html += """<thead><tr><th colspan="2">%s - %s</th></tr></thead>""" % (transaction_obj.players[-1]['player'].transaction_data.source_team_name, time_display)
    for player in transaction_obj.players:
        html += player_table_row_html(player['player'])
    html += """</table><br />"""
    return html

def player_table_row_html(player_obj=None):
    if player_obj is None:
        return ""
    html = """<tr><td>%s</td>""" % player_obj.transaction_data.type
    html += """<td>%s</td>""" % player_obj.name.full
    html += """<td>%s</td>""" % player_obj.editorial_team_abbr
    html += """<td>%s</td></tr>""" % player_obj.display_position
    return html
