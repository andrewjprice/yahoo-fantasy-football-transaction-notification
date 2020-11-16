from datetime import datetime

def timestamp_to_datetime(timestamp):
    return datetime.utcfromtimestamp(int(timestamp)).strftime("%b %d %Y %-I:%M %p")