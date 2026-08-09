## Running the service
### To run in docker
```
docker build -t greatsky .
docker run -d --rm --name greatsky-app -p 8888:80 greatsky
```

### Can also be run locally
```
pip install -r requirements.txt
fastapi dev --port 8888 --host 0.0.0.0
```

### Swagger UI/client
You FastAPI hosts a Swagger UI that you can access via your browser and test the API.

If running locally:

http://localhost:8888/docs
or
http://127.0.0.1:8888/docs

The socket does serve 0.0.0.0, so any host on the same subnet can access it as well.

http://<SERVER_IP>:8888/docs

### OpenAPI json
This will serve the OpenAPI spec.

http://<SERVER_IP>:8888/openapi.json

This spec can be used to auto-generate a python client:
````
$ pip install openapi-python-client
$ openapi-python-client generate --url http://localhost:8888/openapi.json
````
