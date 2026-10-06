import sys
from netmiko import ConnectHandler
import os


host = sys.argv[1]
vdom = sys.argv[2]
multi_vdom = sys.argv[3].lower() == "true"
source_ping = sys.argv[4]
destination_ping = sys.argv[5]

username = os.environ["FORTIOS_SSH_USER"]
password = os.environ["FORTIOS_SSH_PASSWORD"]

conn = ConnectHandler(
    device_type="fortinet",
    host=host,
    username=username,
    password=password,
)

failed_pings = []

if multi_vdom:
    print(f"--- Ping {destination_ping} ---")
    output = conn.send_config_set(
        config_commands=[
            "config vdom",
            f"edit {vdom}",
            f"execute ping-options source {source_ping}",
            f"execute ping {destination_ping}",
            "end"
        ],
        read_timeout=30
    )
else:
    print(f"--- Ping {destination_ping} ---")
    output = conn.send_config_set(
        config_commands=[
            f"execute ping-options source {source_ping}",
            f"execute ping {destination_ping}",
            "end"
    ],
    read_timeout=30
    )
    
success = False

for line in output.splitlines():
    if " 0% packet loss" in line:
        success = True

if success:
    print(f"{destination_ping}: Ping successful")
else:
    print(f"{destination_ping}: Ping failed")
    print(output)
    sys.exit(1)