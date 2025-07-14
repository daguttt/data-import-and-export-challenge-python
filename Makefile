.PHONY: setup start stop clean

setup:
	uv sync
	uv run scripts/generate_sample_data.py

start:
	docker compose up -d
	sleep 3
	uv run main.py

stop:
	docker compose down

clean:
	docker compose down -v
	rm -rf data/output/*
	rm -rf logs/*