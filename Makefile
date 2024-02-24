poetry-export-prod:
	@poetry export -f requirements.txt -o requirements/prod.txt --without-hashes

poetry-export-dev: poetry-export-prod
	@poetry export -f requirements.txt -o requirements/dev.txt --with dev --without-hashes