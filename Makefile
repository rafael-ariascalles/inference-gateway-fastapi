-include .env
export

.PHONY: build run copy-env test

IMAGE_NAME ?= microservice
TAG ?= latest
PORT ?= 8000
DOCKERHUB_USERNAME ?= USER
REGISTRY ?= $(DOCKERHUB_USERNAME)

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

copy-env:
	@if [ ! -f .env ]; then cp .env.example .env; fi;

run: build copy-env
	docker run -it --rm -p $(PORT):$(PORT) --env-file .env --name services $(IMAGE_NAME):$(TAG)

test:
	uv run pytest test/ -v
