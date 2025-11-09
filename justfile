# the path to your venv.  If none, use an empty string
BIN := './venv/bin/'

[no-cd]
pack FILE:
	npx webpack ./{{FILE}} -o . --mode production

install:
	{{BIN}}pip install -r ./REQUIREMENTS.txt

serve:
	{{BIN}}flask run --debug

venv:
	python3 -m venv venv

clean:
	[ ! -d ./__pycache__ ] || rm -r ./__pycache__
	[ ! -d ./.mypy_cache ] || rm -r ./.mypy_cache
	[ ! -d ./app/__pycache__ ] || rm -r ./app/__pycache__
	[ ! -d ./venv ] || rm -rf ./venv
