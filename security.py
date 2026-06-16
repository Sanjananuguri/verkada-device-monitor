import json
from datetime import datetime

# Track suspicious activity
failed_attempts = {}
request_counts = {}

def log_security_event(event_type, details):
    """Log all security events to a file"""
    log_file = "logs/security_log.json"
    
    event = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "event_type": event_type,
        "details": details,
        "severity": get_severity(event_type)
    }
    
    # Read existing logs
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except:
        logs = []
    
    # Append new event
    logs.append(event)
    
    # Write back
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=4)
    
    print(f"🔐 [{event['severity']}] Security Event: {event_type} — {details}")

def get_severity(event_type):
    """Assign severity level to event types"""
    severity_map = {
        "UNAUTHORIZED": "CRITICAL",
        "FORBIDDEN": "HIGH",
        "RATE_LIMITED": "MEDIUM",
        "API_ERROR": "LOW",
        "MASS_OFFLINE": "HIGH",
        "RECONNECTION": "INFO"
    }
    return severity_map.get(event_type, "LOW")

def analyze_api_response(status_code, endpoint):
    """Analyze API response for security anomalies"""
    
    if status_code == 401:
        log_security_event("UNAUTHORIZED", 
            f"Invalid API key used on endpoint: {endpoint}")
    
    elif status_code == 403:
        log_security_event("FORBIDDEN",
            f"Access denied to endpoint: {endpoint}")
    
    elif status_code == 429:
        log_security_event("RATE_LIMITED",
            f"Rate limit hit on endpoint: {endpoint}")
    
    elif status_code >= 500:
        log_security_event("API_ERROR",
            f"Server error {status_code} on endpoint: {endpoint}")

def detect_mass_offline(offline_devices, total_devices):
    """Detect if suspiciously high number of devices go offline"""
    if total_devices == 0:
        return
    
    offline_percentage = (len(offline_devices) / total_devices) * 100
    
    if offline_percentage >= 50:
        log_security_event("MASS_OFFLINE",
            f"{offline_percentage:.1f}% of devices offline — possible network attack or outage!!")

def display_security_summary():
    """Display security log summary"""
    log_file = "logs/security_log.json"
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        print("\n🔐 SECURITY EVENT SUMMARY")
        print("=" * 50)
        print(f"  Total Events : {len(logs)}")
        
        # Count by severity
        severities = {}
        for log in logs:
            sev = log['severity']
            severities[sev] = severities.get(sev, 0) + 1
        
        for sev, count in severities.items():
            print(f"  {sev.ljust(10)} : {count} event(s)")
        
        print("=" * 50)
    
    except:
        print("🔐 No security events logged yet!!")