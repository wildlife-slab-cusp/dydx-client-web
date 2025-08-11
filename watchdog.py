# watchdog.py - updated 2025-08-11

import subprocess
import time
import signal
import sys

def start_process(cmd):
    print(f"Starting: {' '.join(cmd)}", flush=True)
    return subprocess.Popen(cmd)

pipeline = start_process(["python", "pipeline.py"])
webview = start_process(["python", "web_view.py"])

try:
    while True:
        if pipeline.poll() is not None:
            print("pipeline.py stopped — restarting...", flush=True)
            pipeline = start_process(["python", "pipeline.py"])
        if webview.poll() is not None:
            print("web_view.py stopped — restarting...", flush=True)
            webview = start_process(["python", "web_view.py"])
        time.sleep(5)
except KeyboardInterrupt:
    print("Shutting down...", flush=True)
finally:
    for proc in (pipeline, webview):
        try:
            proc.terminate()
        except Exception:
            pass
    sys.exit(0)
