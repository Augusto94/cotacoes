start:
	@docker compose up

shell:
	@docker exec -it cotacoes python manage.py shell

test:
	@docker compose run --rm web pytest --cov --cov-report term-missing --cov-fail-under 90 --disable-pytest-warnings
