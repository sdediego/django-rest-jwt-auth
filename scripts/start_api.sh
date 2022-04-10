#!/usr/bin/bash

set -o errexit
set -o nounset

# Check env variables
echo "DJANGO_ENV is ${DJANGO_ENV}"
echo "Port ${DJANGO_PORT} exposed for DRF JWT Authentication API"

# Set working directory
cd ${PROJECT_DIR}
echo "Change to working directory $(pwd)"

# Run database migrations
python manage.py migrate

if [ ${DJANGO_ENV} = 'development' ]; then
    # Create superuser if not exists
    export DJANGO_SUPERUSER_USERNAME="admin"
    export DJANGO_SUPERUSER_PASSWORD="admin"
    export DJANGO_SUPERUSER_EMAIL="admin@djangorestjwt.com"
    python manage.py createsuperuser --noinput || echo "Superuser already exists."
fi

# Start API server
python manage.py runserver 0.0.0.0:${DJANGO_PORT}
