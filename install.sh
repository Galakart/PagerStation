#!/bin/sh

# Update
sudo apt update
sudo apt dist-upgrade
sudo apt install -y git python3-venv nginx sqlite3 mc

# Rpitx
git clone https://github.com/F5OEO/rpitx
cd rpitx
yes | ./install.sh
cd ..
cp ./rpitx/pocsag ./pocsag
sudo rm -r ./rpitx

# Python
mkdir -p logs
echo Creating venv...
python3 -m venv venv
bash -c "
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
deactivate
"
cp env_example .env

# PyOWM 3.3.0 bug
sed -i 's/assert sender,/assert sender is not None,/g' venv/lib/python*/site-packages/pyowm/weatherapi25/national_weather_alert.py
sed -i 's/assert description,/assert description is not None,/g' venv/lib/python*/site-packages/pyowm/weatherapi25/national_weather_alert.py

# Nginx
sudo unlink /etc/nginx/sites-enabled/default

cat << EOF | sudo tee /etc/nginx/sites-available/pagerstation
server {
    listen 8013;

    location / {
      include proxy_params;
      proxy_pass http://unix:$(pwd)/pagerstation.sock;
    }
}

EOF

sudo ln -s /etc/nginx/sites-available/pagerstation /etc/nginx/sites-enabled
sudo systemctl restart nginx

# Systemd service
cat << EOF | sudo tee /etc/systemd/system/pagerstation.service
[Unit]
Description=PagerStation service
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/gunicorn backend.__main__:app

[Install]
WantedBy=multi-user.target

EOF

echo Installing service...
sudo systemctl daemon-reload
sudo systemctl enable pagerstation

echo ------------------------------------
echo Установка завершена
echo Не забудьте открыть файл .env и установить в нём свои настройки, как написано в README
echo ДЛЯ ЗАВЕРШЕНИЯ НАСТРОЙКИ ТРЕБУЕТСЯ ПЕРЕЗАГРУЗКА RASPBERRY PI!!!
