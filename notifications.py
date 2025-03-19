import requests
from pymongo import MongoClient
from datetime import datetime
import logging

class Notifier:
    def __init__(self, mongo_uri: str, webhook_url: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["hardware_monitor"] if self.client else None
        self.webhook_url = webhook_url

    def send_alert(self, issues: list):
        if not issues:
            return
        
        embed = {
            "title": "Hardware Alert",
            "description": "System issues detected!",
            "color": 16711680,
            "fields": [{"name": i, "value": "Auto-fixed" if "Disk" in i or ("CPU" in i and "Temp" not in i) else "Manual action needed"} for i in issues],
            "footer": {"text": f"Sent at {datetime.utcnow()}"}
        }
        payload = {"embeds": [embed]}
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            msg = f"Alert sent: {', '.join(issues)}"
            if self.db:
                self.db.events.insert_one({"timestamp": datetime.utcnow(), "type": "alert", "message": msg})
            print(msg)
            logging.info(msg)
        except Exception as e:
            print(f"Discord failed: {e}")
            logging.error(f"Discord failed: {e}")