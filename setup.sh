#!/bin/bash

set -e

sudo apt install expect -y

# Instalar mariadb e iniciar el servicio
sudo apt install mariadb-server -y
sudo systemctl start mariadb

# Configurar mariadb
SECURE_MYSQL=$(expect -c "
set timeout 10
spawn sudo mysql_secure_installation

expect \"Enter current password for root (enter for none):\"
send \"\r\"

expect \"Switch to unix_socket authentication [Y/n]\"
send \"y\r\"

expect \"Change the root password? [Y/n]\"
send \"y\r\"

expect \"New password:\"
send \"uvlhubdb_root_password\r\"

expect \"Re-enter new password:\"
send \"uvlhubdb_root_password\r\"

expect \"Remove anonymous users? [Y/n]\"
send \"y\r\"

expect \"Disallow root login remotely? [Y/n]\"
send \"y\r\"

expect \"Remove test database and access to it? [Y/n]\"
send \"y\r\"

expect \"Reload privilege tables now? [Y/n]\"
send \"y\r\"

expect eof
")

echo "$SECURE_MYSQL"

# Configurar la base de datos
sudo mysql -u root -p"uvlhubdb_root_password" <<EOF
DROP DATABASE IF EXISTS rdtdb;
DROP DATABASE IF EXISTS rdtdb_test;
DROP USER IF EXISTS 'rdtdb_user'@'localhost';
CREATE DATABASE rdtdb;
CREATE DATABASE rdtdb_test;
CREATE USER 'rdtdb_user'@'localhost' IDENTIFIED BY 'rdtdb_password';
GRANT ALL PRIVILEGES ON rdtdb.* TO 'rdtdb_user'@'localhost';
GRANT ALL PRIVILEGES ON rdtdb_test.* TO 'rdtdb_user'@'localhost';
FLUSH PRIVILEGES;
EOF


# Configurar entorno de la aplicacion
cp .env.local.example .env

echo "webhook" > .moduleignore

# Crear entorno virtual
sudo apt install python3.12-venv -y
python3 -m venv RaboDeToroHub1venv
source RaboDeToroHub1venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -e ./

# Iniciar la aplicacion
flask db upgrade
rosemary db:seed
flask run --host=0.0.0.0 --port=5000
