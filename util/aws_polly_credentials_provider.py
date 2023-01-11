import json
import os


class AwsPollyCredentialsProvider:
    access_key: str
    secret_key: str

    def __init__(self, json_filepath: str) -> None:
        if not os.path.exists(json_filepath):
            raise RuntimeError(
                f"AWS Polly credentials file doesn't exist: {json_filepath}"
            )

        with open(json_filepath) as f:
            data = json.load(f)
            self.access_key = data["access_key"]
            self.secret_key = data["secret_key"]
