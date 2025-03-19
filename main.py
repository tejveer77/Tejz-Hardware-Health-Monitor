import tkinter as tk
from interface import MonitorGUI
import logging

print("Starting main.py...")

if __name__ == "__main__":
    print("Launching Tejz Hardware Monitor...")
    logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("Starting app")
    try:
        print("Creating Tk root...")
        root = tk.Tk()
        print("Initializing MonitorGUI...")
        app = MonitorGUI(root)
        print("Starting mainloop...")
        root.mainloop()
        print("Mainloop exited.")
    except Exception as e:
        print(f"App crashed: {e}")
        logging.error(f"App crashed: {e}")