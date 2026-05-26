test:
	poetry run pytest .

run:
	poetry run python main.py

extract-translations:
	poetry run pybabel extract -F babel.cfg -o locales/messages.pot .
	poetry run pybabel update -i locales/messages.pot -d locales/
	poetry run python scripts/fill_msgstr.py

compile-translations:
	poetry run pybabel compile -d locales
