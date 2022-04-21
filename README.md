# _Django Rest Framework JSON Web Token Authentication_

This repository contains the code for Django Rest JSON Web Token API backend. The application aims to provide an API backend server for user authentication with JWT (JSON Web Token).

## Documentation

This project has been developed using [Django][django] with [Django Rest Framework][djangorestframework] for the application code and [Postgres][postgres] as relational database.

Code structure implementation follows a [Clean Architecture][cleanarchitecture] approach, emphasizing on code readability, responsibility decoupling and unit testing.

For API backend endpoints documentation refer to the [drf_jwt.yaml][swagger] file in the docs directory.

## Setup

Download source code cloning this repository:
```
git clone https://github.com/sdediego/django-rest-jwt-auth.git
```

## Run the API backend:

Create docker images and execute the containers for development. From the project directory:
```
docker-compose -f ./docker/docker-compose.yaml up --build
```

Shutdown the application and remove network and containers gracefully:
```
docker-compose -f ./docker/docker-compose.yaml down
```

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

[django]: <https://www.djangoproject.com>
[djangorestframework]: <https://www.django-rest-framework.org>
[postgres]: <https://www.postgresql.org>
[cleanarchitecture]: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
[swagger]: <https://github.com/sdediego/django-rest-jwt-auth/blob/main/docs/drf_jwt.yaml>
