#!/bin/sh

echo Upgrading...

sudo service pagerstation stop
git pull --all
bash -c "
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
deactivate
"
sudo service pagerstation start

echo ------------------------------------
echo Upgrade complete
