variable "credentials" {
  description = "My credentials"
  default     = "./keys/my_creds.json"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "gcs_bucket_name" {
  description = "My storage bucket name"
  default     = "terraform-demo-443323-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "project" {
  description = "project name"
  default     = "terraform-demo-443323"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}