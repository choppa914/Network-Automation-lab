import sys
from netmiko import ConnectHandler


def connect(host):
    return ConnectHandler(
        device_type="nokia_srl",
        host=host,
        username="admin",
        password="NokiaSrl1!",
        global_delay_factor=4,
    )


results = []


def check(name, passed):
    results.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}  {name}")


# Which interface on leaf1 faces which spine, and the spine's IP on that link
links = [
    ("spine1", "ethernet-1/49", "192.168.11.1"),
    ("spine2", "ethernet-1/50", "192.168.12.1"),
]

leaf = connect("leaf1")

for spine, iface, spine_ip in links:
    # Check 1: is the interface up?
    out = leaf.send_command(f"show interface {iface} brief")
    check(f"leaf1 {iface} (to {spine}) is up", "up" in out and "down" not in out)

    # Check 2: can leaf1 reach the spine?
    out = leaf.send_command(
        f"ping {spine_ip} network-instance default -c 3", read_timeout=30
    )
    check(f"leaf1 can ping {spine} ({spine_ip})", "0% packet loss" in out)

# Check 3: BGP sessions
out = leaf.send_command("show network-instance default protocols bgp neighbor")
check("leaf1 has an established BGP session", "established" in out.lower())

leaf.disconnect()

print()
print(f"{sum(results)} of {len(results)} checks passed")
sys.exit(0 if all(results) else 1)