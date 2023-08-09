docker-build:
	docker build -t myimage .
	docker build -t setimage -f db-microservices/set-ms/Dockerfile .
	docker build -t deleteimage -f db-microservices/delete-ms/Dockerfile .
	docker build -t getimage -f db-microservices/get-ms/Dockerfile .
	docker build -t kafkaimage -f kafka-microservice/Dockerfile .
	docker build -t kafkaconsumerimage -f kafka-consumer-microservice/Dockerfile .