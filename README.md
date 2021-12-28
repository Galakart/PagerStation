
Pager Station

Что это такое?
-


Нам понадобятся
* собственно сам пейджер Motorola Advisor, купленый на Авито во вменяемом состоянии. 
* Raspberry Pi (а также карта памяти и блок питания)
* Переходник USB-TTL
* Несколько проводков с разъёмами Мама
* Скорее всего немного будет нужен паяльник и соответствующие навыки



Подключение и установка

Берём в одну руку Raspberry, а в другую - один проводок с разъёмами. Подключаем его к штырьку GPIO 4 (который седьмой по счёту). Этот проводок у нас будет играть роль плохонькой антенны.
Что-то из теории антенностроения подсказывает, что лучше бы тут использовать четвертьволновый штырь. Для тех кто забыл, нужно скорость света поделить на частоту в герцах (или 300 поделить на мегагерцы) и поделить ещё на 4. 
То есть, при примерной частоте 159 МГц, считаем: 300 / 159 / 4 = 47 сантиметров, желательная длина штыря антенны. И размещать его лучше вертикально.

Далее как обычно, раскатываем на карту памяти образ свежей Raspberry Pi OS (она же Raspbian). Подключаемся по SSH в консоль и первым делом запустим настройки. 
sudo raspi-config

Главное что тут нужно поменять
- сдвинуть доступную GPU Memory на минимум, освободив оперативку
- расширить файловую систему на всю карту памяти (Expand Filesystem)
- по желанию можно разогнать процессор
если потребуется, перезагрузить систему

настраиваем часовой пояс, выбираем свой регион
sudo dpkg-reconfigure tzdata

обновляем систему
sudo apt update
sudo apt dist-upgrade
sudo apt autoremove

по желанию ставим русский язык
sudo apt install language-pack-ru
sudo update-locale LANG=ru_RU.UTF-8

устанавливаем необходимое ПО
sudo apt install git python3-venv python3-dev mariadb-server mariadb-client redis-server memcached nginx

заходим в папку, где мы будем размещать программу (например создаём новую папку "services" в домашней папке, после чего заходим туда) и клонируем себе этот репозиторий
git clone REPONAME
и заходим в папку с ним 
cd REPONAME

установим rpitx
git clone https://github.com/F5OEO/rpitx
cd rpitx
./install.sh
ожидаем окончания сборки, соглашаемся на модификацию config.txt, обязательно перезагружаемся
sudo reboot

снова заходим в папку REPONAME. rpitx уже установлен, нам нужно взять только бинарник и положить его в корень проекта (где req.txt)
cp ./rpitx/pocsag ./pocsag
больше папка rpitx нам не нужна. Удаляем её и навешиваем атрибут на бинарник
sudo rm -r ./rpitx
sudo chmod +x pocsag

Настроим mariadb
sudo mysql_secure_installation
на вопрос о текущем пароле (current root password) просто нажать enter (без пароля)
установить пароль рута (set root password) - говорим no, мы всё равно не будем использовать учётку рута
на все остальные вопросы отвечаем yes
создадим юзера БД, допустим с именем admin и паролем password, с возможностью доступа только из localhost
sudo mariadb
GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;
FLUSH PRIVILEGES;
exit

при необходимости доступа за пределами localhost, учётку нужно называть как
'admin'@'%'
поменяем конфиг
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
выставим параметр
bind-address 0.0.0.0
sudo service mariadb restart

в папке с проектом создадим виртуальное окружение:
python3 -m venv venv
source venv/bin/activate
убедимся что мы в окружении - зелёное venv слева от командной строки (проверять в дальнейшем)

скопируем файл системных переменных и дадим атрибут:
cp .env_example .env
chmod 600 .env

Заодно сгенерируем и скопируем себе новый SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
отредактируем файл
nano .env
обращаем внимание, что до и после знака равно не должно быть пробелов

SECRET_KEY - сюда вставляем только что сгенерированый секретный ключ
DEBUG - для вывода отладочных сообщений - True. В рабочей версии и для лучшей безопасности лучше оставить False
DB_NAME, DB_HOST, DB_USER, DB_PASS - параметры доступа к БД
TOKEN_OWM - токен OpenWeatherMap (TODO как получить)
WEATHER_CITY - город для прогноза погоды (TODO формат)

в настройках часовой пояс и язык

cp celery.example.conf celery.conf
поменять параметр CELERY_BIN
/home/pi/services/pagerstation/venv/bin/celery

установим зависимости
pip install -r requirements.txt

проведём миграции БД и соберём статику
python manage.py migrate
python manage.py collectstatic

также необходимо создать суперюзера
python manage.py createsuperuser

Можно проверить как работает сервер Django
python manage.py runserver 0:80
И планировщик Celery
celery -A pagerstation worker -l info -B


Далее условимся что папка с проектом находится по пути /home/pi/services/pagerstation
Если она расположена в другом месте, меняем этот путь во всех нижеприведённых конфигах


Создадим конфиг nginx, удалив при этом стандартный
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-available/pagerstation

Вставим текст

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

Создадим ярлык и проверим конфигурацию
sudo ln -s /etc/nginx/sites-available/pagerstation /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

Создадим конфиг для gunicorn
sudo nano /etc/systemd/system/pagerstation_gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target
PartOf=pagerstation.service

[Service]
User=root
Group=www-data
WorkingDirectory=/home/pi/services/pagerstation
ExecStart=/home/pi/services/pagerstation/venv/bin/gunicorn --access-logfile - --workers 2 --bind unix:/home/pi/services/pagerstation/pagerstation.sock pagerstation.wsgi:application

[Install]
WantedBy=multi-user.target

Конфиг для воркера celery
sudo nano /etc/systemd/system/pagerstation_celery_worker.service

[Unit]
Description= PagerStation Celery Worker Service
After=network.target
PartOf=pagerstation.service

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

Конфиг для планировщика celery
sudo nano /etc/systemd/system/pagerstation_celery_beat.service

[Unit]
Description=PagerStation Celery Beat Service
After=network.target
PartOf=pagerstation.service

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

И один конфиг, чтобы править всеми
sudo nano /etc/systemd/system/pagerstation.service
[Unit]
Description=PagerStation Group Service
Wants=pagerstation_gunicorn.service
Wants=pagerstation_celery_worker.service
Wants=pagerstation_celery_beat.service

[Service]
Type=oneshot
ExecStart=/bin/echo "Starting PagerStation instances"
RemainAfterExit=yes
StandardOutput=journal

[Install]
WantedBy=multi-user.target

Папки для логов
sudo mkdir /var/log/celery
sudo chown pi:pi /var/log/celery
sudo chmod 0755 /var/log/celery

Обновим и поставим в автозапуск стартовые скрипты
sudo systemctl daemon-reload
sudo systemctl enable pagerstation

Теперь для ручного запуска можно вводить команду
sudo service pagerstation start или sudo systemctl start pagerstation

Настройка завершена, для полной надёжности можно перезапустить систему, сервис стартует автоматически.




Первоначальная настройка
-




Перепрограммирование пейджера
-




Отправка сообщений
-





Использованные источники

https://github.com/F5OEO/rpitx 
Hot Pixel https://www.youtube.com/watch?v=ukmvlHdsdfc
SinuX https://mysku.ru/blog/diy/88396.html https://mysku.ru/blog/diy/88811.html 
https://cxem.net/telefon/2-28.php

https://pyowm.readthedocs.io/en/latest/v3/code-recipes.html#weather_forecasts

