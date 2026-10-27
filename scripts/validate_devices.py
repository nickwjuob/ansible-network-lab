from collections import Counter
from ipaddress import ip_address
from pathlib import Path
import sys

import yaml


devices_file = Path("data/devices.yml")
required_fields = ("name", "management_ip", "platform", "role")
errors = []

try:
    data = yaml.safe_load(devices_file.read_text())
except (OSError, yaml.YAMLError) as exc:
    print(f"ERROR: Cannot read {devices_file}: {exc}")
    sys.exit(1)

if not isinstance(data, dict) or not isinstance(data.get("devices"), list):
    print("ERROR: Expected a YAML object containing a devices list.")
    sys.exit(1)

devices = data["devices"]

if not devices:
    errors.append("devices list must not be empty")

names = []
management_ips = []

for index, device in enumerate(devices, start=1):
    if not isinstance(device, dict):
        errors.append(f"devices[{index}] must be an object")
        continue

    for field in required_fields:
        value = device.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"devices[{index}]: missing or empty field '{field}'")

    name = device.get("name")
    if isinstance(name, str) and name.strip():
        names.append(name.strip())

    address = device.get("management_ip")
    if isinstance(address, str) and address.strip():
        try:
            ip_address(address.strip())
            management_ips.append(address.strip())
        except ValueError:
            errors.append(
                f"devices[{index}]: invalid management_ip '{address}'"
            )

for name, count in Counter(names).items():
    if count > 1:
        errors.append(f"duplicate device name: {name}")

for address, count in Counter(management_ips).items():
    if count > 1:
        errors.append(f"duplicate management IP: {address}")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print(f"OK: validated {len(devices)} devices")
