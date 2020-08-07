variable "profile" {
    type        = "string"
    description = "AWS Profile"

    default = "datasp"
}

variable "region" {
    type        = "string"
    description = "Region"
    default = "us-east-1"
}

variable "key_name" {
    type        = "string"
    description = "Temporary key name"
    default = "airflow_terraform"
}

variable "instance_type" {
    type    = "string"
    default = "t3.large"
    # default = "t3.micro"
}


variable "airflow_username" {}

variable "airflow_password" {}
