run-directly:
	DATABASE_URL=development.sqlite flask --app flaskr/app run --debug
run-with-docker:
	docker build -t reviews .
	docker run --env-file development.env -p 127.0.0.1:5000:5000 reviews
test:
	ruff check flaskr
	ruff format flaskr
	cd flaskr; pytest .
clean:
	find . -type d -name ".pytest_cache" | xargs rm -rf
	find . -type d -name ".ruff_cache" | xargs rm -rf
	find . -type d -name "__pycache__" | xargs rm -rf
deploy:
	fly deploy --ha=false