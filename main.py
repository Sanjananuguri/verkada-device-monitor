import requests
import json
from datetime import datetime
from config import BASE_URL, HEADERS
from monitor import check_camera_health, display_health_report, log_offline_devices
from alerts import check_alert_threshold, send_console_alert, generate_alert_summary
from dashboard import display_dashboard
from security import analyze_api_response, detect_mass_offline, display_security_summary

def get_all_cameras():
    endpoint = f"{BASE_URL}/cameras/v1/devices"
    print(f"[{datetime.now()}] Fetching cameras...")
    response = requests.get(endpoint, headers=HEADERS)
    
    analyze_api_response(response.status_code, endpoint)
    
    if response.status_code == 200:
        print("✅ Connection successful!!")
        return response.json()
    elif response.status_code == 401:
        print("❌ Invalid API Key — check your .env file!!")
        return None
    elif response.status_code == 403:
        print("❌ No permission — check your Org ID!!")
        return None
    else:
        print(f"❌ Error: {response.status_code}")
        return None

def get_all_doors():
    endpoint = f"{BASE_URL}/access/v1/doors"
    print(f"[{datetime.now()}] Fetching doors...")
    response = requests.get(endpoint, headers=HEADERS)
    
    analyze_api_response(response.status_code, endpoint)
    
    if response.status_code == 200:
        print("✅ Doors fetched successfully!!")
        return response.json()
    else:
        print(f"❌ Error fetching doors: {response.status_code}")
        return None

if __name__ == "__main__":
    print("🎥 Verkada Device Health Monitor Starting...")
    print("=" * 50)
    
    cameras = get_all_cameras()
    doors = get_all_doors()

    if cameras:
        online, offline = check_camera_health(cameras)
        total = len(online) + len(offline)
        health_score = display_health_report(online, offline, total)
        log_offline_devices(offline)
        
        detect_mass_offline(offline, total)
        
        critical = check_alert_threshold(offline)
        send_console_alert(critical)
        generate_alert_summary(health_score, offline, critical)
        
        display_dashboard(online, offline, health_score, doors)
    
    display_security_summary()