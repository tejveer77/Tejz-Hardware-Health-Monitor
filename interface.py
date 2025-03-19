import tkinter as tk
from tkinter import ttk
from monitor import HardwareMonitor
from autofix import AutoFix
from notifications import Notifier
import json
import logging
from datetime import datetime, timedelta
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            print(f"Running from PyInstaller temp folder: {base_path}")
        else:
            base_path = os.path.abspath(".")
            print(f"Running from local folder: {base_path}")
        full_path = os.path.join(base_path, relative_path)
        print(f"Looking for config at: {full_path}")
        return full_path
    except Exception as e:
        print(f"Path error: {e}")
        raise

class MonitorGUI:
    def __init__(self, root):
        print("Initializing MonitorGUI...")
        self.root = root
        self.root.title("Tejz Hardware Monitor")  
        self.root.geometry("400x350")
        
        config_path = resource_path("config.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        
        self.monitor = HardwareMonitor()
        self.autofix = AutoFix(config["mongo_uri"])
        self.notifier = Notifier(config["mongo_uri"], config["discord_webhook_url"])
        self.refresh_interval = config["refresh_interval"]

        self.cpu_label = ttk.Label(root, text="CPU: 0%")
        self.cpu_label.pack(pady=5)
        self.temp_label = ttk.Label(root, text="CPU Temp: N/A")
        self.temp_label.pack(pady=5)
        self.ram_label = ttk.Label(root, text="RAM: 0%")
        self.ram_label.pack(pady=5)
        self.disk_label = ttk.Label(root, text="Disk Free: 0 GB")
        self.disk_label.pack(pady=5)
        self.status_label = ttk.Label(root, text="Status: Starting...", foreground="blue")
        self.status_label.pack(pady=10)

        ttk.Button(root, text="Refresh Now", command=self.update_gui).pack(pady=5)
        ttk.Button(root, text="Show Logs", command=self.show_log).pack(pady=5)

        print("GUI initialized, starting updates...")
        self.update_gui()

    def update_gui(self):
        print("Updating GUI...")
        stats = self.monitor.get_stats()
        self.cpu_label.config(text=f"CPU: {stats.get('cpu', 0):.1f}%")
        temp = stats.get('cpu_temp', None)
        self.temp_label.config(text=f"CPU Temp: {temp:.1f}°C" if temp else "CPU Temp: N/A")
        self.ram_label.config(text=f"RAM: {stats.get('ram', 0):.1f}%")
        self.disk_label.config(text=f"Disk Free: {stats.get('disk_free', 0):.2f} GB")
        
        issues = self.monitor.check_issues(stats)
        if issues:
            self.status_label.config(text=f"Issues: {', '.join(issues)}", foreground="red")
            self.autofix.fix_issues(issues)
            self.notifier.send_alert(issues)
        else:
            self.status_label.config(text="Status: All Good", foreground="green")
        
        print("Scheduling next update...")
        self.root.after(self.refresh_interval, self.update_gui)

    def show_log(self):
        print("Showing logs...")
        log_window = tk.Toplevel(self.root)
        log_window.title("Recent Logs")
        log_text = tk.Text(log_window, height=15, width=60)
        log_text.pack(pady=10)
        
        if self.monitor.db is not None:
            try:
                time_threshold = datetime.utcnow() - timedelta(hours=24)
                events = self.monitor.db.events.find(
                    {"timestamp": {"$gte": time_threshold}}
                ).sort("timestamp", -1).limit(10)
                event_list = list(events)
                if not event_list:
                    log_text.insert(tk.END, "No issues in the last 24 hours.\n")
                else:
                    for event in event_list:
                        log_text.insert(tk.END, f"{event['timestamp']}: {event['type'].upper()} - {event['message']}\n")
                        print(f"Log entry: {event['timestamp']} - {event['message']}")
            except Exception as e:
                log_text.insert(tk.END, f"Error fetching logs: {e}\n")
        else:
            log_text.insert(tk.END, "No DB connection, logs unavailable.\n")
        log_text.config(state="disabled")