from stelvio.app import StelvioApp
from stelvio.config import AwsConfig, StelvioAppConfig
from stelvio.aws.api_gateway import Api

app = StelvioApp("my-first-stelvio-app")


@app.config
def configuration(env: str) -> StelvioAppConfig:
    return StelvioAppConfig(
        aws=AwsConfig(
            profile=None,                # Use environment variables or default profile
        ),
    )


@app.run
def run() -> None:
    # Simple API exposed via API Gateway
    api = Api(
        "MyApi",
    )
    # Create a Route for GET /
    api.route("get", "/", "functions/api.handler")
