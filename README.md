
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
python manage.py collectstatic

pocsag binary to the root folder (where req.txt is, for example)

celery -A pagerstation worker -l info -B

sudo nano /etc/systemd/system/pagerstation_gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/user/cloudproject
ExecStart=/home/user/cloudproject/cloudenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/user/myproject/myproject.sock myproject.wsgi:application

[Install]
WantedBy=multi-user.target



sudo apt install nginx

sudo nano /etc/nginx/sites-available/pagerstation_backend

server {
listen 80;
server_name ;

location = /favicon.ico { access_log off; log_not_found off; }
location /static/ {
root /root/cloudproject;
}

location / {
include proxy_params;
proxy_pass http://unix:/root/cloudproject/cloudproject.sock;
}
}

sudo ln -s /etc/nginx/sites-available/pagerstation_backend /etc/nginx/sites-enabled

sudo nginx -t
sudo systemctl restart nginx



sudo nano /etc/systemd/system/pagerstation_celery_worker.service

[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=pi
Group=pi
EnvironmentFile=/home/user/pagerstation/celery.conf
WorkingDirectory=/home/user/pagerstation
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target

sudo nano /etc/systemd/system/pagerstation_celery_beat.service

[Unit]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=pi
Group=pi
EnvironmentFile=/home/user/pagerstation/celery.conf
WorkingDirectory=/home/user/pagerstation
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
    --pidfile=${CELERYBEAT_PID_FILE} \
    --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
Restart=always

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable pagerstation_gunicorn
sudo systemctl enable pagerstation_celery_worker
sudo systemctl enable pagerstation_celery_beat
sudo service pagerstation_gunicorn start
sudo service pagerstation_celery_worker start
sudo service pagerstation_celery_beat start

