import json
import os
from teamsproxy import TeamsProxy

def lambda_handler(event, context):
    url = os.getenv("TEAMS_URL")
    payload = json.loads(event.get("body"))
    tp = TeamsProxy(payload)
    
    msg = "Successfully forwarded to teams"
    sc = 202

    result = tp.send2teams(url)

    if not result:
        msg = "something went wrong"
        sc = 500

    return {
        "statusCode": sc,
        "body": msg
    }
