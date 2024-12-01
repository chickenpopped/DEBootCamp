terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.12.0"
    }
  }
}

provider "google" {
    credentials = "./keys/my_creds.json"
  project = "terraform-demo-443323"
  region  = "us-"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-443323-bucket"
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}