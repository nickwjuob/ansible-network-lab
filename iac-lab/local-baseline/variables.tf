variable "baseline_filename" {
  description = "Output filename for the network baseline"
  type        = string
  default     = "network-baseline.txt"

  validation {
    condition     = length(trimspace(var.baseline_filename)) > 0
    error_message = "baseline_filename must not be empty."
  }
}
