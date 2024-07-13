# Rick and Morty Character API

This application provides a REST API to fetch Rick and Morty characters from [rickandmortyapi](https://rickandmortyapi.com/) with the following filter:

  species = Human

  status = Alive 

  name of origin starts with Earth

## Building the Docker Image

Build the Docker image:
```
docker build -t rick-and-morty-api:latest .
```

Run the Docker container:
```
docker run -p 3000:3000 rick-and-morty-api
```
The application will now be running on `http://localhost:3000`

## Setup a local Kind Kubernetes instance

Assuming you have kind installed, run the following to create an instance:
```
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```
Install the nginx-ingress controller
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```
Load the locally built image to the kind instance
```
kind load docker-image rick-and-morty-api
```

## Deploy the manifests
Apply the Kubernetes manifests to first create the target namespace then the service, ingress and deployment:
```
kubectl apply -f yamls/namespace.yaml
```
```
kubectl apply -f yamls/ -n rick-and-morty
```

## Deploy using Helm chart

```
helm upgrade --install rick-and-morty-api ./helm --create-namespace --namespace rick-and-morty
```

## REST API Endpoints

1. Healthcheck
  * Endpoint: `/healthcheck`
  * Method: GET
  * Description: Returns the health status of the application.
  * Example: `curl http://localhost:3000/healthcheck`

2. Filtered Characters
  * Endpoint: `/characters`
  * Method: GET
  * Description: Returns a list of Rick and Morty characters filtered by the following criteria:
    * Species is "Human"
    * Status is "Alive"
    * Origin starts with "Earth"
  * Example: `curl http://localhost:3000/characters`

## Fetching Data

To fetch data from the API, you can use curl in the terminal or any HTTP client. Here are examples using curl:

1. Healthcheck:
curl http://localhost:3000/healthcheck
2. Filtered Characters:
curl http://localhost:3000/characters
You can also use a web browser to access these endpoints by navigating to the URLs.

## GitHub Actions Workflow

This project includes a GitHub Actions workflow that automatically tests and deploys the application. The workflow is triggered on pushes to the main branch and on pull requests targeting the main branch.

### Workflow Steps:

1. **Build Docker Image**: Builds the application's Docker image.
2. **Create Kind Cluster**: Sets up a local Kubernetes cluster using Kind.
3. **Load Docker Image**: Loads the built Docker image into the Kind cluster.
4. **Install Ingress NGINX**: Deploys the NGINX Ingress Controller to the cluster.
5. **Deploy Application**: Uses Helm to deploy the application to the Kind cluster.
6. **Run Tests**: Executes a series of tests against the deployed application.

### Test Suite

The test suite performs the following checks:

1. **Healthcheck**: Ensures the `/api/healthcheck` endpoint returns a 200 status code, verifying that the application is up and running.

2. **JSON Integrity**: Validates that the `/api/characters` endpoint returns well-formed JSON data.

3. **Data Structure**: Checks that the returned JSON has the expected structure, including the presence of required fields (name, location, image).

4. **Response Content**: Counts the number of characters returned and ensures the response is not empty.

These tests serve several purposes:
* Verify that the application is deployed correctly and accessible.
* Ensure that the API is functioning as expected and returning the correct data format.
* Catch any potential regressions or changes in the API response structure.
* Validate the integrity and consistency of the data returned by the API.