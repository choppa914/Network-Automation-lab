import sys
import time
from netmiko import ConnectHandler

# Usage: python automation/toggle_interface.py <router> <interface> <seconds_down>
router = sys.argv[1] if len(sys.argv) > 1 else "spine1"
interface = sys.argv[2] if len(sys.argv) > 2 else "ethernet-1/1"
down_seconds = int(sys.argv[3]) if len(sys.argv) > 3 else 60


def push(conn, commands):
    conn.send_config_set(commands, exit_config_mode=False)
    conn.commit()


conn = ConnectHandler(
    device_type="nokia_srl",
    host=router,
    username="admin",
    password="NokiaSrl1!",
    global_delay_factor=4,
)

try:
    print(f"Disabling {router} {interface} ...")
    push(conn, [f"set / interface {interface} admin-state disable"])
    print(f"Waiting {down_seconds} seconds. Watch Grafana now.")
    time.sleep(down_seconds)
finally:
    # Runs even if something above crashed or you pressed Ctrl+C
    print(f"Enabling {router} {interface} ...")
    push(conn, [f"set / interface {interface} admin-state enable"])
    conn.disconnect()
    print("Done. Interface restored.")