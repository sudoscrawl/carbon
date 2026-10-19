test:
	pytest .

run:
	python main.py

extract-translations:
	pybabel extract -F babel.cfg -o locales/messages.pot .
	pybabel update -i locales/messages.pot -d locales/
	python scripts/fill_msgstr.py

compile-translations:
	pybabel compile -d locales
