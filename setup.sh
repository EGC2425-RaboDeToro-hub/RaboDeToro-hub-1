#!/bin/bash

set -e

# Pedir al usuario el nombre de la base de datos y la contraseña
read -p "Ingrese el nombre de la base de datos: " dbname
read -p "Ingrese el nombre del usuario que desea usar en la base de datos: " dbuser
read -sp "Ingrese la contraseña para el usuario root de la base de datos: " dbrootpassword
echo
read -sp "Confirme la contraseña para el usuario root de la base de datos: " dbrootpassword_confirm
echo

# Verificar que las contraseñas coincidan
if [ "$dbrootpassword" != "$dbrootpassword_confirm" ]; then
    echo "Las contraseñas no coinciden. Inténtelo de nuevo."
    exit 1
fi

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
send \"$dbrootpassword\r\"

expect \"Re-enter new password:\"
send \"$dbrootpassword\r\"

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
sudo mysql -u root -p"$dbrootpassword" <<EOF
DROP DATABASE IF EXISTS $dbname;
DROP DATABASE IF EXISTS ${dbname}_test;
DROP USER IF EXISTS '$dbuser'@'localhost';
CREATE DATABASE $dbname;
CREATE DATABASE ${dbname}_test;
CREATE USER '$dbuser'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
GRANT ALL PRIVILEGES ON $dbname.* TO '$dbuser'@'localhost';
GRANT ALL PRIVILEGES ON ${dbname}_test.* TO '$dbuser'@'localhost';
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
rosemary db:reset -y
rosemary db:migrate
rosemary db:seed
flask db upgrade
flask run --host=0.0.0.0 --port=5000

