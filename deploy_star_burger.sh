#!/bin/bash

set -e

echo "Check repo updates"
git pull

echo "Preparing frontend"
sudo docker build -t frontend -f frontend/Dockerfile.prod.frontend .
sudo docker run -v $(pwd)/bundles:/app/bundles frontend

echo "Preparing backend"
sudo docker-compose -f docker-compose.prod.yml down
sudo docker-compose -f docker-compose.prod.yml up -d
sudo docker exec -t django python manage.py migrate
sudo docker cp -a django:/app/staticfiles/. /var/www/frontend/
container_id=$(docker create frontend)
docker cp -a $container_id:/frontend/bundles/. /var/www/frontend/
docker rm -v $container_id

echo "Cleaning unused docker items"
sudo docker system prune -f

sudo systemctl reload nginx

last_commit=$(git log -1 --pretty=format:'%H')
commit_author=$(git log -1 --pretty=format:'%an')
source backend/.env.prod

curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d '{"environment": "production", "revision": "'"$last_commit"'", "rollbar_name": "art.gilyazov", "local_username": "'"$commit_author"'", "comment": "star burger deployment"}'

echo "Deploy successfully finished."

