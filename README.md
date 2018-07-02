# Tete-a-tete Chat
Intensive course from KTS Studio, summer 2018

## How to run

##### 1. Install Python and JS dependencies:

```
pip install -r requirements.txt
npm install
```

##### 2. Build project

```
python manage.py migrate
npm run build-prod
```

##### 3. Run servers

* application-server:
 
```
gunicorn -b ip:port(127.0.0.1:8000) chat.wsgi:application
```

* proxy-server (nginx config), static:  

```
server {
    listen 80;

    # server_name my.chat.dev;
    server_name 127.0.0.1:80;
    # the domain name it will serve for
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;

    location / {
        proxy_pass    http://127.0.0.1:8000/;
    }

    location /static {
        alias    /Users/artyom/Projects/Chat/build/;
    }

    location /media {
        alias    /Users/artyom/Projects/Chat/media/;
    }
}
```

* websocket-server (daphne) && database for ws sessions (redis):

  Run your redis on default port, then
  
```
daphne -b ip(127.0.0.1) -p port(8001) chat.asgi:application
```