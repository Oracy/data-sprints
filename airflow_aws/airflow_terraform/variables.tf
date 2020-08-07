variable "region" {
    type = "string"
}

variable "instance_name" {
    type = "string"
}

variable "instance_type" {
    type = "string"
}

variable "key_name" {
    type = "string"
}

variable "private_nameserver" {
    type = "string"
    default = "airflow_terraform"
}

variable "vpc_id" {
    type = "string"
    default = "vpc-91aceff4"
    description = "Data Network"
}

variable "public_subnet_ids" {
    type = "string"
    default = "subnet-ff7ae388"
    description = "Data Network Public"
}
