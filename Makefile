.PHONY: build run push-docker-hub build-push-image

IMAGE_NAME ?= microservice
TAG ?= latest
DOCKERHUB_USERNAME ?= USER
REGISTRY ?= $(DOCKERHUB_USERNAME)

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run: build
	docker run -it --rm -p 8000:8000 --name services $(IMAGE_NAME):$(TAG)
