#!/bin/bash
cd /home/projects/arrplat
echo "更新代码"
git pull
echo "构建node服务"
yarn
yarn run build
echo "更新配置"
./bin/startup.js
echo "重启web前端"
pm2 restart 0
echo "重启api"
supervisorctl restart arrplat-api
