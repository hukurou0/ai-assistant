# API 開発

## 起動

docker run -it -v /home/huku/ai-assistant/api:/app ai-assistant-api /bin/bash

## ファイル更新

docker build -t ai-assistant-api ./api

## dalete data

psql -U myuser -d mydatabase

delete from app_user;

jwt token を local storage に入れて
そこにトークンがあったらログインとして扱われる
