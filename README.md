# FeedzE
Yet another feed reader like Feedly

## Features
* Use JWT Authentication.
* Add RSS link to fetch feed items and news.
* Bookmark and Favorite feed items.
* Using async task for updating feeds. 

## Models

### User
Save user data

### Feed
Save feeds data like title, link, image of a feed.

### FeedItem
Save feed items like title, link, description, author data's of news.

## API Documents
We use Django REST Framework ability to generation OpenAPI schemas.
We're using [Swagger UI](https://swagger.io/tools/swagger-ui/) to generate HTML documentation pages from OpenAPI schemas.
API documets are [here](http://localhost:8000/docs/).

## Built with
* Python
* Django
* Django Rest Framework
* Postgresql
* Docker
* Celery
* RabbitMQ

## Prerequisites
you need to install:

* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

## Getting Started
We use Docker and Docker Compose for easy deployment:
```shell
docker-compose up --build
```
