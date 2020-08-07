#!/bin/sh
set -e

USERNAME="${airflow_username}"
PASSWD="${airflow_password}"

if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    echo "Not root" > /home/ubuntu/log.log
    exit 1
fi

PASSCRYPT=$(perl -e 'print crypt($ARGV[0], "password")' $PASSWD)
useradd -p "$PASSCRYPT" -d /home/"$USERNAME" -m -g users -s /bin/bash "$USERNAME"
usermod -aG docker $USERNAME
usermod -aG sudo $USERNAME

echo "" >> /etc/ssh/sshd_config
echo "    Match User $USERNAME" >> /etc/ssh/sshd_config
echo "    PasswordAuthentication yes" >> /etc/ssh/sshd_config
echo "    KbdInteractiveAuthentication yes" >> /etc/ssh/sshd_config

service ssh restart

unlink /etc/localtime
ln -s /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
