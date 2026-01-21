variable "cribl_client_id" {
  description = "Cribl Cloud API Client ID"
  type        = string
  sensitive   = true
}

variable "cribl_client_secret" {
  description = "Cribl Cloud API Client Secret"
  type        = string
  sensitive   = true
}

variable "cribl_cloud_org" {
  description = "Cribl Cloud Organization ID"
  type        = string
}

variable "worker_group_name" {
  description = "Display name for the worker group"
  type        = string
  default     = "quickstart-worker-group"
}

variable "worker_group_id" {
  description = "Unique identifier for the worker group (no spaces, lowercase)"
  type        = string
  default     = "quickstart-wg"
}

variable "worker_group_description" {
  description = "Description for the worker group"
  type        = string
  default     = "Worker group created via Terraform quickstart"
}

variable "pack_source" {
  description = "Pack source URL from Pack Dispensary"
  type        = string
  default     = "git+https://github.com/criblpacks/cribl-palo-alto-networks.git"
}

variable "pack_id" {
  description = "Pack identifier (name)"
  type        = string
  default     = "cribl-palo-alto-networks"
}
