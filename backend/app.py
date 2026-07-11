from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from log_parser import parse_log_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stats")
async def get_stats(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    stats = parse_log_file(content)
    if stats["LINES"] > 0 and stats["INFO"] == 0 and stats["WARN"] == 0 and stats["ERROR"] == 0:
        return {"error": "Invalid log file format. Expected format: YYYY-MM-DD HH:MM:SS [LEVEL] IP message"}
    return stats
