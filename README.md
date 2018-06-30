# Tete-a-tete Chat
Intensive course from KTS Studio, summer 2018

## How to run

* application-server:
 
```
gunicorn -b ip:port chat.wsgi:application
```

* proxy-server (nginx config):  

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
