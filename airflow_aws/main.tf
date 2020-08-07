provider "aws" {
    region = "${var.region}"
}

module "airflow" {
    source = "./airflow_terraform"
    region = "${var.region}"

    instance_name = "Airflow"
    instance_type = "${var.instance_type}"

    key_name = "${var.key_name}"
    airflow_username = "${var.airflow_username}"
    airflow_password = "${var.airflow_password}"

}
