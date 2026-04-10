#!/bin/sh
# Injeta a variável de ambiente BACKEND_URL no index.html em runtime
# Isso permite que o frontend saiba a URL do backend sem rebuild

BACKEND_URL=${BACKEND_URL:-"http://localhost:8000"}

# Usa arquivo temporário para evitar problemas com barras na URL
TMP=$(mktemp)
sed "s|window.BACKEND_URL || \"http://localhost:8000\"|\"${BACKEND_URL}\"|g" \
    /usr/share/nginx/html/index.html > "$TMP"
mv "$TMP" /usr/share/nginx/html/index.html

nginx -g "daemon off;"