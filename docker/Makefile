build:
	docker build --network host --compress -t jodafons/root-cern:latest .
	docker build --network host --compress -t jodafons/root-cern:base .
push:
	docker push jodafons/root-cern:latest
	docker push jodafons/root-cern:base
