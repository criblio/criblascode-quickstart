# Stream Commit and Deploy Configuration
# Handles the commit and deploy workflow for the main Stream worker group

# Step 1: Commit all Stream configuration changes
resource "criblio_commit" "stream_commit" {
  effective = true
  group     = var.worker_group_id # Uses the main Stream group (default)
  message   = "Deploy Stream configuration via Terraform - iteration ${timestamp()}"

  depends_on = [
    # Stream destinations
    # criblio_pack.aws_pan_logs

  ]
}

# Step 2: Get the latest config version after commit
data "criblio_config_version" "stream_config_version" {
  id         = var.worker_group_id
  depends_on = [criblio_commit.stream_commit]
}

# Step 3: Deploy the committed configuration
resource "criblio_deploy" "stream_deploy" {
  id      = var.worker_group_id
  version = length(data.criblio_config_version.stream_config_version.items) > 0 ? data.criblio_config_version.stream_config_version.items[length(data.criblio_config_version.stream_config_version.items) - 1] : "default"

  depends_on = [
    data.criblio_config_version.stream_config_version
  ]
}
