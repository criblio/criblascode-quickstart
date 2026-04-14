# Create a new worker group in Cribl Cloud
# resource "criblio_group" "worker_group" {
#   id          = var.worker_group_id
#   name        = var.worker_group_name
#   description = var.worker_group_description
#   product     = "stream"
# }

# figure out how to manipulate pack vars per WG and add examples
#**********
# Install the AWS Pan pack into the worker group
resource "criblio_pack" "aws_pan_logs" {
  id       = var.pack_id
  group_id = var.worker_group_name
  source   = var.pack_source
  spec     = "main"
}

#From The dispensary 
resource "criblio_pack" "bedrock" {
  id = "cribl-bedrock-io"
  group_id = var.worker_group_name
  source = "https://packs.cribl.io/dl/cribl-aws-bedrock-io/2.0.0/cribl-aws-bedrock-io-2.0.0.crbl"
  
}

