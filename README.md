
Pager Station

python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
chmod 600 .env

sudo apt install redis-server

sudo apt install mariadb-server mariadb-client
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

pocsag binary to the project folder (where req.txt is, for example)

celery -A pagerstation worker -l info -B

sudo nano /etc/systemd/system/pagerstation_gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/pi/services/pagerstation
ExecStart=/home/pi/services/pagerstation/venv/bin/gunicorn --access-logfile - --workers 2 --bind unix:/home/pi/services/pagerstation/pagerstation.sock pagerstation.wsgi:application

[Install]
WantedBy=multi-user.target



sudo apt install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-available/pagerstation

server {
listen 80;
server_name ;

location = /favicon.ico { access_log off; log_not_found off; }
location /static/ {
root /home/pi/services/pagerstation;
}

location / {
include proxy_params;
proxy_pass http://unix:/home/pi/services/pagerstation/pagerstation.sock;
}
}

sudo ln -s /etc/nginx/sites-available/pagerstation /etc/nginx/sites-enabled

sudo nginx -t
sudo systemctl restart nginx



sudo nano /etc/systemd/system/pagerstation_celery_worker.service

[Unit]
Description= PagerStation Celery Worker Service
After=network.target

[Service]
Type=forking
User=pi
Group=pi
EnvironmentFile=/home/pi/services/pagerstation/celery.conf
WorkingDirectory=/home/pi/services/pagerstation
RuntimeDirectory=celery
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
Description=PagerStation Celery Beat Service
After=network.target

[Service]
Type=simple
User=pi
Group=pi
EnvironmentFile=/home/pi/services/pagerstation/celery.conf
WorkingDirectory=/home/pi/services/pagerstation
RuntimeDirectory=celery
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
    --pidfile=${CELERYBEAT_PID_FILE} \
    --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
Restart=always

[Install]
WantedBy=multi-user.target

sudo mkdir /var/log/celery
sudo chown pi:pi /var/log/celery
sudo chmod 0755 /var/log/celery

sudo systemctl daemon-reload
sudo systemctl enable pagerstation_gunicorn
sudo systemctl enable pagerstation_celery_worker
sudo systemctl enable pagerstation_celery_beat
sudo service pagerstation_gunicorn start
sudo service pagerstation_celery_worker start
sudo service pagerstation_celery_beat start

