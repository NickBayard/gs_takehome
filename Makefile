clean:
	for d in $$(find . -name __pycache__ -type d); do rm -r $$d; done

run:
	fastapi dev --port 8888 --host 0.0.0.0
