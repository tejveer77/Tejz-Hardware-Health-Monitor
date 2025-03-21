# Tejz Hardware Monitor

## Overview
Tejz Hardware Monitor is a standalone Windows application designed for IT system diagnostics and automation. Packaged as an executable, it provides a Tkinter-based GUI to monitor hardware metrics (CPU, memory, disk, temperature) in real time, detect issues, auto-resolve them, and send Discord alerts. Tailored for IT support, this tool combines monitoring, logging, and proactive fixes in one portable package.

---

## Features
- **Real-Time Monitoring**: Tracks CPU usage (%), RAM usage (%), disk free space (GB), and CPU temperature (°C, if available).
- **Issue Detection**: Identifies high usage or critical states with customizable thresholds.
- **Auto-Fix**: Automatically resolves detected issues (e.g., kills high-CPU processes—configurable via dependencies).
- **Notifications**: Sends alerts to Discord via webhook when issues arise.
- **Log Viewer**: Displays recent system events from MongoDB in a GUI window.
- **Portable**: Runs as a single `.exe`—no Python or dependency installation required.

---

## Requirements
- **OS**: Windows (tested on Windows 10/11).
- **Dependencies**: None for end-users—all bundled in the `.exe`.
- **Configuration**: Requires a `config.json` file (template provided).


## Installation
1. **Download**:
   - Clone or download this repository:
     ```bash
     git clone https://github.com/tejveer77/Tejz-Hardware-Health-Monitor.git
     Please include you discord webhook in config.json
2. After cloning please go to folder and open dist folder
3. Make sure config.json and main.exe are present in dist
4. Click main.exe and you will be able to run it

## If it throws Error and app crashes
Please clone repository and delete dist folder but make sure you don't delete config.json
After that please run the following command in terminal
```bash
pyinstaller -F --add-data "config.json;." main.py -n HardwareMonitor
After installation is done please place config.json in dist folder and you can run main.exe now .
     
     
