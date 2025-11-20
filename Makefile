include .env

generate-data:
	uv run python -m src/scripts/generate_data
