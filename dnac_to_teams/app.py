import json
import os
from teamsproxy import TeamsProxy

def lambda_handler(event, context):
    url = os.getenv("TEAMS_URL")
    payload = json.loads(event.get("body"))
    tp = TeamsProxy(payload)
    
    msg = "ok"
    sc = 200

    result = tp.send2teams(url)

    if not result:
        msg = "something went wrong"
        sc = 500

    return {
        "statusCode": sc,
        "body": json.dumps({"message": msg}),
        "headers": {
            "Content-Type": "application/json"
        }
    }
