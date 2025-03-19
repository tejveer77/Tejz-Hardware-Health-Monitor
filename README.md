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

## Run .exe
- Open the dist folder
-- Select main.exe
-- Wait for few seconds 
-- Refresh it to view real time information
-- View App Log to see issues occured in last 24 hours

## Installation
1. **Download**:
   - Clone or download this repository:
     ```bash
     git clone https://github.com/tejveer77/Tejz-Hardware-Monitor.git
     Please include you discord webhook in config.json
     