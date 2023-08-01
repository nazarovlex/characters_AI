
.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	sudo docker-compose up

.PHONY: stop
stop:
	docker-compose stop

.PHONY: clean
clean:
	sudo rm -rf .pg_data

.PHONY: restart
restart:
	make build
	make start