import json
import requests
import datetime

from pyadaptivecards.card import AdaptiveCard
from pyadaptivecards.container import ColumnSet
from pyadaptivecards.components import TextBlock, Column
from pyadaptivecards.options import FontWeight
from pyadaptivecards.actions import OpenUrl



class TeamsProxy:


    def __init__(self, dnac_payload):
        self.dnac_payload = dnac_payload


    def parse(self):
        event_id = self.dnac_payload.get("eventId")
        event_link = self.dnac_payload.get("ciscoDnaEventLink")
        timestamp = datetime.datetime.fromtimestamp(self.dnac_payload.get("timestamp")/1000).strftime("%d-%m-%Y %H:%M:%S")
        details_titles = self.dnac_payload.get("details").keys()
        details_values = self.dnac_payload.get("details").values()

        title = TextBlock(text=event_id, weight=FontWeight.BOLDER)
        col_titles = Column(items=[TextBlock(text=k, weight=FontWeight.BOLDER) for k in ["Timestamp"]+list(details_titles)])
        col_values = Column(items=[TextBlock(text=v, wrap=True) for v in [timestamp]+list(details_values)])
        col_set = ColumnSet(columns=[col_titles, col_values])
        link = OpenUrl(url=event_link, title="Click to see details in DNAC")
        #link = TextBlock(text=event_link)
        card = AdaptiveCard(body=[title, col_set], actions=[link]).to_dict()
        card["msTeams"] = {"width": "full"}
        acard = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": card
                }
            ]
        }
        #print(json.dumps(acard, indent=1))
        return acard


    def send2teams(self, teams_url):
        payload = self.parse()
        r = requests.post(teams_url, json=payload)
        print(r.ok)
        if r.ok:
            return True
        raise Exception("Could not send message to MS Teams")
