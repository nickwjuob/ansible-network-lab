terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

locals {
  devices_data = yamldecode(
    file("${path.module}/../../data/devices.yml")
  )

  devices = {
    for device in local.devices_data.devices :
    device.name => device
  }
}

resource "local_file" "network_baseline" {
  filename = "${path.module}/${var.baseline_filename}"

  content = join("\n", concat(
    ["Network Engineering Baseline"],
    [
      for name in sort(keys(local.devices)) :
      "${name}: ${local.devices[name].management_ip}"
    ]
  ))
}
