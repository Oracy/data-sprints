provider "aws" {
        region = "${var.region}"
}

data "template_cloudinit_config" "airflow_terraform" {
    gzip            = true
    base64_encode   = true

    part {
        content_type = "text/x-shellscript"
        content      = "${data.template_file.airflow_terraform.rendered}"
    }
}

resource "aws_instance" "airflow_terraform" {
    ami             = "ami-0ef38e7f365e6e6d4" # Amazon_v2
    instance_type   = "${var.instance_type}"

    vpc_security_group_ids  = ["${aws_security_group.airflow_terraform.id}"]
    subnet_id               = "${var.public_subnet_ids}"
    associate_public_ip_address = true

    key_name  = "${var.key_name}"
    user_data = "${data.template_cloudinit_config.airflow_terraform.rendered}"

    tags {
        Name = "${var.instance_name}"
    }
}
