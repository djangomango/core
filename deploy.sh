#!/bin/sh

chmod +x wait-for-it.sh
chmod +x rebuild.sh

docker-compose -f docker-compose.frontend-build.yml run node npm run prod
docker-compose -f docker-compose.frontend-build.yml run node npm run maizzle:build
docker system prune -a -f
docker-compose -f docker-compose.prod.ssl.yml --env-file prod.env up
