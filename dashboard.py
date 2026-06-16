from datetime import datetime

def display_dashboard(online, offline, health_score, doors=None):
    """Display a clean visual dashboard in terminal"""
    
    total = len(online) + len(offline)
    
    # Health bar visual
    filled = int(health_score / 10)
    empty = 10 - filled
    health_bar = "█" * filled + "░" * empty
    
    print("\n")
    print("╔══════════════════════════════════════════════════╗")
    print("║       🎥 VERKADA DEVICE HEALTH DASHBOARD 🎥      ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  🕐 Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}          ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  📷 CAMERAS                                      ║")
    print(f"║  Total Devices  : {str(total).ljust(30)} ║")
    print(f"║  ✅ Online      : {str(len(online)).ljust(30)} ║")
    print(f"║  ❌ Offline     : {str(len(offline)).ljust(30)} ║")
    print(f"║  💯 Health      : [{health_bar}] {health_score}%       ║")
    print("╠══════════════════════════════════════════════════╣")
    
    if doors:
        total_doors = len(doors.get('doors', []))
        print(f"║  🚪 ACCESS CONTROL                               ║")
        print(f"║  Total Doors    : {str(total_doors).ljust(30)} ║")
        print("╠══════════════════════════════════════════════════╣")
    
    if offline:
        print(f"║  ⚠️  OFFLINE DEVICES                              ║")
        for device in offline:
            name = device['name'][:25].ljust(25)
            print(f"║  → {name} | {device['location'][:15].ljust(15)} ║")
    else:
        print("║  🎉 ALL DEVICES ONLINE — FLEET HEALTHY!!         ║")
    
    print("╚══════════════════════════════════════════════════╝")
    print("\n")