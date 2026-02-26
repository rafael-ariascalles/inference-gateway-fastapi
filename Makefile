.PHONY: build run push-docker-hub build-push-image

IMAGE_NAME ?= microservice
TAG ?= latest
DOCKERHUB_USERNAME ?= USER
REGISTRY ?= $(DOCKERHUB_USERNAME)

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

copy-env:
	if [ ! -f .env ]; then
		cp .env.example .env
	fi

run: build copy-env
	docker run -it --rm -p 8000:8000 --env-file .env --name services $(IMAGE_NAME):$(TAG)
