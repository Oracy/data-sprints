resource "aws_security_group" "airflow_terraform" {
    name        = "airflow_terraform"
    description = "airflow sandbox Security Group"

    vpc_id = "${var.vpc_id}"
}

resource "aws_security_group_rule" "allow-all-output" {
    type        = "egress"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "-1"

    security_group_id = "${aws_security_group.airflow_terraform.id}"
}

resource "aws_security_group_rule" "allow-ssh-input" {
    type        = "ingress"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

    security_group_id = "${aws_security_group.airflow_terraform.id}"
}

resource "aws_security_group_rule" "allow-web-input" {
    type        = "ingress"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

    security_group_id = "${aws_security_group.airflow_terraform.id}"
}

resource "aws_security_group_rule" "allow-pg-input" {
    type        = "ingress"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

    security_group_id = "${aws_security_group.airflow_terraform.id}"
}
