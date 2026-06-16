import json
import csv
from datetime import datetime
from config import BASE_URL, HEADERS, OFFLINE_THRESHOLD
import requests

# Track how many times each device has been offline
offline_counts = {}

def check_camera_health(cameras):
    """Check each camera and flag offline ones"""
    offline = []
    online = []

    for camera in cameras.get('cameras', []):
        device_id = camera.get('device_id')
        name = camera.get('name', 'Unknown')
        status = camera.get('status', 'unknown')
        location = camera.get('location', 'Unknown')

        if status != 'online':
            # Count how many times this device has been offline
            offline_counts[device_id] = offline_counts.get(device_id, 0) + 1

            offline.append({
                'device_id': device_id,
                'name': name,
                'status': status,
                'location': location,
                'offline_count': offline_counts[device_id],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            # Reset counter if back online
            offline_counts[device_id] = 0
            online.append(name)

    return online, offline

def calculate_health_score(total, online_count):
    """Calculate fleet health percentage"""
    if total == 0:
        return 0
    return round((online_count / total) * 100, 1)

def log_offline_devices(offline_devices):
    """Log offline devices to a CSV file"""
    if not offline_devices:
        return

    log_file = f"logs/offline_log_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(log_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'timestamp', 'device_id', 'name', 
            'status', 'location', 'offline_count'
        ])
        
        # Write header only if file is new/empty
        if f.tell() == 0:
            writer.writeheader()
        
        writer.writerows(offline_devices)
    
    print(f"📝 Logged {len(offline_devices)} offline devices to {log_file}")

def display_health_report(online, offline, total):
    """Print a clean health report to terminal"""
    health_score = calculate_health_score(total, len(online))
    
    print("\n" + "=" * 50)
    print("       VERKADA DEVICE HEALTH REPORT")
    print("=" * 50)
    print(f"🕐 Time        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📷 Total       : {total}")
    print(f"✅ Online      : {len(online)}")
    print(f"❌ Offline     : {len(offline)}")
    print(f"💯 Health Score: {health_score}%")
    print("=" * 50)

    if offline:
        print("\n⚠️  OFFLINE DEVICES:")
        for device in offline:
            print(f"  → {device['name']} | {device['location']} | Offline Count: {device['offline_count']}")
    else:
        print("\n🎉 All devices are online!!")
    
    print("=" * 50 + "\n")
    
    return health_score