from pathlib import Path
import yaml

devices_file = Path("data/devices.yml")
inventory_file = Path("inventory.ini")

devices = yaml.safe_load(devices_file.read_text())["devices"]

lines = ["[cisco_routers]"]

for device in devices:
    lines.append(
        f'{device["name"]} ansible_host={device["management_ip"]}'
    )

lines.extend([
    "",
    "[cisco_routers:vars]",
    "ansible_connection=ansible.netcommon.network_cli",
    "ansible_network_os=cisco.ios.ios",
    "ansible_user=admin",
    "",
])

inventory_file.write_text("\n".join(lines))
print(f"Generated {inventory_file} from {devices_file}")
