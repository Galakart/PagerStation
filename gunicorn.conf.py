from multiprocessing import cpu_count

# Socket Path
bind = 'unix:./pagerstation.sock'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'
preload_app = True

proxy_headers=True
forwarded_allow_ips='*'

# Logging Options
loglevel = 'info'
# accesslog = './logs/applog.log'
errorlog =  './logs/applog.log'
