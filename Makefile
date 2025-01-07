.PHONY: setup dev build deploy clean

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r data/requirements.txt
	cd site && npm install

dev:
	. .venv/bin/activate && cd data && python scripts/grab_data.py
	cd site && npm run dev

build:
	. .venv/bin/activate && cd data && python scripts/grab_data.py
	cd site && npm run build

deploy:
	make build
	cd site && npm run deploy

clean:
	rm -rf .venv
	rm -rf site/node_modules