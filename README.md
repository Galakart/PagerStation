
Pager Station

python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
chmod 600 .env

https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04-ru
sudo apt install redis-server

celery -A pagerstation worker -l info -B
