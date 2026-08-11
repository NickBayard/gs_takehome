## Running the service
### To run in docker
```
# from the same directory as the Dockerfile
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

## Design Description

#### REST API
The service API uses a RESTful interface.  Many of the available service API libraries directly support REST APIs, which also enables the use of OpenAPI features.  In this case, I selected FastAPI, which is a modern, featureful Python API framework that comes with several features built-in:
- serves a SwaggerUI page for testing the REST API
- outputs OpenAPI json content, which can be used to auto-generate an SDK in several popular languages
- native support for Pydantic models
- can serve on localhost or remote host IPs on a bound port.  Users can run the service locally or access it on a remote machine
- can serve on a UNIX domain socket using uvicorn or gunicorn for local process clients only
- can scale using an asyncio server (uvicorn), process server (guvicorn) or load balancer (nginx)

The API currently supports multiple devices.  In order to operate on a device, a client must acquire a new session.  If the device is in use, the session request will be denied.  (This does provide the opportunity to queue session requests until devices are no longer in use.)  Currently, only one device can be tied to a session.  The service also supports multiple, concurrent sessions meaning multiple clients can be running tests on their independent devices at the same time.  Users must close the session when they are done with the device. There is currently no mechanism to timeout and/or garbage collect abandoned sessions.

#### Database
The service uses a database to synchronize and store state between request handler instances.
Currently the database is only used to store session and device model data.  APIs that operate on
waveforms, biases (current), and weights (memory) do not store state in the data store and only
interface with connected instruments via the drivers.

For this simple design I wanted a lightweight database that as persistent and didn't require a complex schema design.  SQLite is file-based and uses a client library rather than a server process,
but is a relational database.  I found LevelDB, which is the same but a NoSQL (key value) data store.
I'd never used LevelDB before, but found the library interface very simple and met the needs of
a demo service like this one.

In order to demonstrate how we can swap out similar databases, I created a common interface for
key-value datastores (greatsky/db/base.py) that allows any concrete class implementation (e.g. greatsky/db/leveldb.py) to be built using a factory function (greatsky/db/factory.py).  The database type is selected using a value in config.yaml.  Changing the underlying database implementation doesn't affect the business logic at all.

A set of lightweight Object Relational Mapping (ORM) classes are included that allow callers to perform CRUD operations on database entries using Python objects.

#### Drivers
The drivers that instrument hardware (e.g. AWG, scope, memory controller) had overlapping interfaces.  For example, a scope can be used to capture a waveform, but an RFSoC can generate and capture waveforms.  Each of the network device components did not necessarily need the entire interface from connected devices (e.g. an output node does not need set_waveform on an RFSoC) and often needed a combination of interfaces from multiple devices (e.g. an output node may be connected to a scope for waveform capture and a voltage source to set bias current).

In order to allow the replacement or addition of hardware drivers used by device components (inputs, outputs, edges) and limit the API scope that each component has access to, I used a flyweight design pattern to aggregate APIs from multiple drivers into one component driver that then limited the API access to those input drivers.   For example, in greatsky/drivers/base.py, OutputDriver is composed of the interfaces from BiasDriver and WaveformOutDriver.  BiasDriver has interfaces for managing bias current and WaveformOutDriver has interfaces for waveform capture.  If WaveformOutDriver were connected to an RFSoC, the driver interfaces to set a new waveform would not be exposed to OutputDriver. (Mocked instrument drivers and poll_driver are located in greatsky/drivers/lib.py.)

### Missing Features
All of the features below would be considered required for a production quality product but were left out in order to reasonably time-box the project.

Authentication and authorization (AuthN/AuthZ) were not implmented.  There is an ORM class for the User resource type that contains a unique username, hashed password and list of permissions. I considered two potential designs for authentication:
1. Basic HTTP Auth - Users provide a username and password (ideally over an encrypted connected like TLS) to a /login or /token endpoint.  The service hashes the password and checks against the User object in the database.  If there's a match, the service returns a JSON Web Token (JWT) containing the username and expiration timestamp.  Subsequent requests from that user must contain this JWT in the Authorization header.
2. OAuth2  flow - The same as Basic HTTP Auth except unauthorized requests are served a form, which need to be populated with a username and password and returned to the /token API.  The database verification and JWT response are the same.
3. I had also considered using Google OAuth2 with OpenID Connect scope.  The main benefit here is that users with Google accounts (or Google Workspaces domain accounts) could use those accounts to authenticate with the service. This would redirect requests from the service to Google for browser login.   This workflow is significantly more complex.  Ideally we'd use the password workflow with Google, but I don't think that is supported any longer as it's less secure.

There are no unit tests nor integration tests.  Integration tests would ideally start a service instance and exercise the endpoints to validate behavior.

There is no logging performed.  Should an internal server error occur (caught or uncaught) there would be no way to troubleshoot the error without logging breadcrumbs and tracebacks.  This service uses sessions to aggregate multiple requests.  This is an excellent candidate for [wide event logging](https://loggingsucks.com/), which collects breadcrumb events, errors and other observability events during a handler execution and emits them at the end of the handler lifetime as a single JSON object.  Each session would get its own log file containing a set of JSON wide event log objects from each request.  This allows us to separate logs for concurrent sessions more easily and view log events from concurrent requests within the same session in separate entries (rather than interleaving through a single log file).

Typically there would be detailed docstring for request handlers, classes, methods, functions, etc.  This provides detail to readers about the intent and usage of components of the service.

I also did not bother to write API annotations for the OpenAPI spec.  The API path parameters, query parameters, and body models can be annotated so that the SwaggerUI and OpenAI spec contain additional detain about these elements.

## Improvements
1. Queuing - As mentioned earlier, failed POST session requests could be queued.  Clients would need to poll to see when a new session is successfully acquired.  This would ensure their place in line for that device, whether specified or allocated.
2. Client SDK - Thin API client can be autogenerated using the OpenAPI spec, but there should be an additional SDK to manage sessions and user authentication/authorization.  This wasn't a requirement for the project but would be required so that human and automated users could consume the service.
3. Connected instruments should be included in the device model.  Currently this information is obfuscated from the device model and relies on poll_driver to discover the instrument type.  By attaching instrument classes to each devices's model, different devices could use different instruments (e.g.  device A uses an AWG for input waveform and device B uses an RFSoC).  New APIs would be used to change the connected instrument for each function (waveform input, waveform capture, bias current, weights/memory) without overwriting the entire device model.

## Assumptions
- The number of input and output nodes is low (e.g. less than 10).
- There are only input and output nodes that are directly connected without intermediate network layers.
- Users MUST know the unique ID of any node or edge that they want to instrument.  For example, to set an edge weight, a caller must specify the name of the edge, which contains the name of the two nodes (input or output) that the edge connects.

## Risks

#### Scalability
1. A network with tens of thousands of inputs/outputs and millions of edges cannot have the shape specified with explicit names in this way.  Nor can we store that shape in a database entry in the simple way that's being done now.  Setting the weight/memory of every edge would require multiple API calls to set weights for millions of edges.
2. This implementation isn't suitable for more than a handful of client connections and tens of devices.  To scale up, the implementation should use asyncio handlers and server (uvicorn) with multiple worker processes.  For additional scaling, the service could take on a distributed design with a load balancer (like nginx) dispatching work across multiple hosts and a dedicated database service on its own host.  An orchestrator like Kubernetes is useful for managing distributed services like this.
3. The database selected uses a local file for the datastore, similar to how SQLite does but for a key-value data store instead of a relational one. This restricts one process from accessing the data store at a time.  A data store with a server process would allow simultaneous access by multiple processes or multiple hosts.

#### Waveform capture
Returning a waveform in a response body is really not practical as the size of this data can be quite large. Returning actual binary data of this size requires streaming so that data can be chunked back to the caller.  There are two mechanisms by which we could stream waveforms to the client.
1. Use a websocket to send the stream from service to client
2. Serve a dedicated endpoint where callers can make a request to stream the waveform.  Unless the waveform capture driver can return chunks of the waveform stream, the service would need to buffer the captured waveform, which can consume a lot of memory.  Alternatively, the service could temporarily save the waveform to disk and then stream that back to the client.