import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta

def parse_log_file(text: str):
    lines = text.splitlines()
    stats = {
        "LINES": len(lines),
        "INFO": 0,
        "WARN": 0,
        "ERROR": 0,
        "unique_ips": 0,
        "top_ips": [],
        "last_errors": [],
        "error_histogram": {},
    }

    # Regex pour parser les logs: date time [LEVEL] IP message
    log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (\d+\.\d+\.\d+\.\d+) (.+)')
    
    errors = []
    ips = set()
    ip_counts = Counter()
    error_times = []
    
    for line in lines:
        match = log_pattern.match(line.strip())
        if not match:
            # Si la ligne ne correspond pas, ignorer ou compter comme invalide
            continue
        date_str, level, ip, message = match.groups()
        try:
            timestamp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue  # Skip invalid dates
        
        ips.add(ip)
        ip_counts[ip] += 1
        
        if level == 'INFO':
            stats["INFO"] += 1
        elif level == 'ERROR':
            stats["ERROR"] += 1
            errors.append(message)
            error_times.append(timestamp)
        elif level == 'WARN':
            stats["WARN"] += 1
    
    # Last 5 errors
    stats["last_errors"] = errors[-5:]
    
    # Unique IPs
    stats["unique_ips"] = len(ips)
    
    # Top 5 IPs
    stats["top_ips"] = ip_counts.most_common(5)
    
    # Error histograms
    now = datetime.now()
    
    # Per minute (last 60 minutes)
    start_minute = now - timedelta(minutes=60)
    minute_counts = defaultdict(int)
    for t in error_times:
        if t >= start_minute:
            minute_key = t.strftime('%Y-%m-%d %H:%M:00')
            minute_counts[minute_key] += 1
    stats["error_histogram_minute"] = dict(minute_counts)
    
    # Per hour (last 24 hours)
    start_hour = now - timedelta(hours=24)
    hour_counts = defaultdict(int)
    for t in error_times:
        if t >= start_hour:
            hour_key = t.strftime('%Y-%m-%d %H:00:00')
            hour_counts[hour_key] += 1
    stats["error_histogram_hour"] = dict(hour_counts)
    
    # Per day (last 7 days)
    start_day = now - timedelta(days=7)
    day_counts = defaultdict(int)
    for t in error_times:
        if t >= start_day:
            day_key = t.strftime('%Y-%m-%d')
            day_counts[day_key] += 1
    stats["error_histogram_day"] = dict(day_counts)
    
    return stats