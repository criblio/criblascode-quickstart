terraform {
  required_version = ">= 1.0"

  required_providers {
    criblio = {
      source = "criblio/criblio"
      # version = ">= 1.0.0"
    }
  }
}

provider "criblio" {
  client_id       = var.cribl_client_id
  client_secret   = var.cribl_client_secret
  organization_id = var.cribl_cloud_org
  workspace_id    = var.workspace_id
  cloud_domain    = "cribl-staging.cloud"
}
