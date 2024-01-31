#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static
apt-get update
apt-get install -y nginx
ufw allow 'Nginx HTTP'
echo "Hello World!" > /var/www/html/index.html
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
echo "server {
        listen 80;
        listen [::]:80;

        server_name _;

        error_page 404 /404.html;
        add_header X-Served-By 475984-web-01;

        location / {
            root /var/www/html;
            index index.html;
        }

        location /redirect_me {
            return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
        }

        location /404 {
            root /var/www/html;
            internal;
        }

        location /hbnb_static {
            alias /data/web_static/current/;
        }
}" >/etc/nginx/sites-enabled/default
service nginx restart
