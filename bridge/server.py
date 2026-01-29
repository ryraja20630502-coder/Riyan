import subprocess
from fastapi import FastAPI

app = FastAPI()

process = None

@app.get("/start")
def start_assistant():
    global process
    if not process:
        process = subprocess.Popen(["python", "../assistant/riyan.py"])
        return {"status": "Riyan started"}
    return {"status": "Already running"}

@app.get("/stop")
def stop_assistant():
    global process
    if process:
        process.terminate()
        process = None
        return {"status": "Stopped"}
    return {"status": "Not running"}
