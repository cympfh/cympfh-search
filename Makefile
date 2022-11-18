build:
	docker build -t cympfh-search:latest .

PORT := 8083

run:
	docker run --rm \
		-p 8083:8083 \
		-v ~/git/cympfh.github.io/:/git/cympfh.github.io/ \
		cympfh-search:latest
