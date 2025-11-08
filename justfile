# the path to your venv.  If none, use an empty string
BIN := './venv/bin/'

install:
	{{BIN}}pip install -r ./REQUIREMENTS.txt

serve:
	{{BIN}}flask run --debug
