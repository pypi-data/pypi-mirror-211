#!\bin\bat

pdoc src\easy_tui -o docs
python -m build
python -m twine upload dist/* -u __token__ -p %PYPI_AUTH_TOKEN%