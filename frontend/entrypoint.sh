#!/bin/sh
export BACKEND_URL=${BACKEND_URL:-"http://localhost:8000"}

envsubst '${BACKEND_URL}' < /usr/share/nginx/html/index.html.tmpl \
    > /usr/share/nginx/html/index.html

chmod 644 /usr/share/nginx/html/index.html

nginx -g "daemon off;"