import psutil
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import logging
import json
import subprocess

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class HardwareMonitor:
    def __init__(self, config_path: str = "config.json"):
        print("Initializing HardwareMonitor...")
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.thresholds = self.config["thresholds"]
        
        try:
            self.client = MongoClient(self.config["mongo_uri"], serverSelectionTimeoutMS=5000)
            self.client.server_info()
            self.db = self.client["hardware_monitor"]
            print("MongoDB connected!")
            logging.info("Connected to MongoDB")
        except ConnectionFailure as e:
            print(f"MongoDB failed: {e}. Running in fallback mode.")
            logging.error(f"MongoDB failed: {e}")
            self.db = None

    def get_cpu_temp(self):
        print("Fetching CPU temp...")
        try:
            ps_command = "powershell -Command \"Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace 'root/wmi' | Select-Object -Property CurrentTemperature | ForEach-Object { ($_.CurrentTemperature / 10) - 273.15 }\""
            result = subprocess.check_output(ps_command, shell=True, text=True, stderr=subprocess.STDOUT)
            temp = float(result.strip())
            print(f"Got CPU temp: {temp}°C")
            logging.info(f"CPU temp from WMI: {temp}°C")
            return temp
        except (subprocess.CalledProcessError, ValueError, Exception) as e:
            cpu_usage = psutil.cpu_percent(interval=1)
            estimated_temp = 35 + (cpu_usage * 0.55)
            print(f"WMI temp failed: {e}. Using estimate: {estimated_temp}°C")
            logging.warning(f"WMI temp failed: {e}. Estimated temp: {estimated_temp}°C")
            return estimated_temp

    def get_stats(self):
        print("Getting stats...")
        stats = {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "disk_free": psutil.disk_usage("C:/").free / (1024 ** 3),
            "cpu_temp": self.get_cpu_temp(),
            "timestamp": datetime.utcnow()
        }
        try:
            if self.db is not None:
                self.db.stats.insert_one(stats)
            logging.info(f"Stats logged: {stats}")
            print("Stats retrieved:", stats)
        except Exception as e:
            print(f"DB insert failed: {e}")
            logging.error(f"DB insert failed: {e}")
        return stats

    def check_issues(self, stats: dict):
        print("Checking issues...")
        print(f"CPU: {stats['cpu']} vs {self.thresholds['cpu']}, RAM: {stats['ram']} vs {self.thresholds['ram']}, Disk: {stats['disk_free']} vs {self.thresholds['disk_free']}, Temp: {stats['cpu_temp']} vs 85")
        issues = []
        if stats.get("cpu", 0) > self.thresholds["cpu"]:
            issues.append(f"High CPU: {stats['cpu']}%")
        if stats.get("ram", 0) > self.thresholds["ram"]:
            issues.append(f"High RAM: {stats['ram']}%")
        if stats.get("disk_free", 0) < self.thresholds["disk_free"]:
            issues.append(f"Low Disk: {stats['disk_free']:.2f} GB")
        if stats.get("cpu_temp") and stats["cpu_temp"] > 85:
            issues.append(f"High Temp: {stats['cpu_temp']:.1f}°C")
        
        try:
            if self.db is not None and issues:
                for issue in issues:
                    self.db.events.insert_one({"timestamp": datetime.utcnow(), "type": "issue", "message": issue})
        except Exception as e:
            print(f"DB event insert failed: {e}")
            logging.error(f"DB event insert failed: {e}")
        
        logging.warning(f"Issues: {issues}")
        print("Issues checked:", issues)
        return issues