venv:
	[[ ! -d ".venv" ]] && python3 -m venv .venv || true
	.venv/bin/pip install -r requirements.txt


build: venv
	.venv/bin/python3 -m build


distribute:
	.venv/bin/python3 -m twine upload --repository pypi dist/*


clean:
	rm -rf dist


clean-all: clean
	rm -rf .venv


.SILENT: venv build distribute clean clean-all
.PHONY: venv build distribute clean clean-all
