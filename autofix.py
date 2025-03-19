import subprocess
import psutil
from pymongo import MongoClient
from datetime import datetime
import os
import logging

class AutoFix:
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["hardware_monitor"] if self.client else None

    def clear_temp_files(self):
        try:
            temp_dir = os.environ["TEMP"]
            subprocess.run(f"del /q /f {temp_dir}\\*.*", shell=True, check=True)
            msg = "Cleared temp files"
            if self.db:
                self.db.events.insert_one({"timestamp": datetime.utcnow(), "type": "fix", "message": msg})
            print(msg)
            logging.info(msg)
        except Exception as e:
            print(f"Temp clear failed: {e}")

    def kill_high_cpu_process(self):
        try:
            processes = [(p.pid, p.cpu_percent()) for p in psutil.process_iter()]
            top_pid, top_cpu = max(processes, key=lambda x: x[1])
            if top_cpu > 50:
                psutil.Process(top_pid).terminate()
                msg = f"Killed PID {top_pid} ({top_cpu}%)"
                if self.db:
                    self.db.events.insert_one({"timestamp": datetime.utcnow(), "type": "fix", "message": msg})
                print(msg)
                logging.info(msg)
        except Exception as e:
            print(f"Kill failed: {e}")

    def fix_issues(self, issues: list):
        for issue in issues:
            if "Disk" in issue:
                self.clear_temp_files()
            elif "CPU" in issue and "Temp" not in issue:
                self.kill_high_cpu_process()
            elif "Temp" in issue:
                print("High temp detected - manual cooling required!")
                logging.warning("High temp - no auto-fix available")