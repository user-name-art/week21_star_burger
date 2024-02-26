#!/bin/bash

set -e

echo "Star-burger deploy started."

cd /opt/week21_star_burger/
git pull git@github.com:user-name-art/week21_star_burger.git
source ./.venv/bin/activate
pip install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
python manage.py collectstatic --noinput
python manage.py migrate --noinput
sudo systemctl restart star-burger.service
sudo systemctl reload nginx

last_commit=$(git log -1 --pretty=format:'%H')
commit_author=$(git log -1 --pretty=format:'%an')
source .env

curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d '{"environment": "production", "revision": "'"$last_commit"'", "rollbar_name": "art.gilyazov", "local_username": "'"$commit_author"'", "comment": "star burger deployment", "status>

echo "Deploy successfully finished."
