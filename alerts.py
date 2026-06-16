from datetime import datetime
from config import OFFLINE_THRESHOLD

def check_alert_threshold(offline_devices):
    """Only alert if device has been offline multiple times"""
    critical = []
    
    for device in offline_devices:
        if device['offline_count'] >= OFFLINE_THRESHOLD:
            critical.append(device)
    
    return critical

def send_console_alert(critical_devices):
    """Send alert to terminal for critical offline devices"""
    if not critical_devices:
        return
    
    print("\n🚨 CRITICAL ALERT 🚨")
    print("=" * 50)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔴 {len(critical_devices)} device(s) critically offline!!")
    print("=" * 50)
    
    for device in critical_devices:
        print(f"""
   Device   : {device['name']}
   Location : {device['location']}
    Status   : {device['status']}
   Offline  : {device['offline_count']} consecutive checks
   Since    : {device['timestamp']}
        """)
    print("=" * 50)

def generate_alert_summary(health_score, offline_devices, critical_devices):
    """Generate a summary of current alert status"""
    
    if health_score == 100:
        level = "🟢 HEALTHY"
    elif health_score >= 80:
        level = "🟡 WARNING"
    else:
        level = "🔴 CRITICAL"
    
    print(f"\n ALERT SUMMARY")
    print(f"  Status Level  : {level}")
    print(f"  Health Score  : {health_score}%")
    print(f"  Offline Devices : {len(offline_devices)}")
    print(f"  Critical Alerts : {len(critical_devices)}")
