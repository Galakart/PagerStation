
Pager Station

python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
chmod 600 .env

https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04-ru
sudo apt install redis-server

sudo apt install memcached
pip install pymemcache

install mariadb with user
sudo apt install mariadb-server mariadb-client
https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04-ru 
sudo mysql_secure_installation
current root password - none (нажать enter)
set root password - no
остальные yes
sudo mariadb
GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;
FLUSH PRIVILEGES;
exit

sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
bind-address 0.0.0.0
sudo service mariadb restart

python manage.py migrate
python manage.py createsuperuser

pocsag binary to the root folder (where req.txt is, for example)

celery -A pagerstation worker -l info -B
