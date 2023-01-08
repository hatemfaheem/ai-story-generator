import json
import os


class OpenAICredentialsProvider:
    organization: str
    api_key: str

    def __init__(self, json_filepath: str) -> None:
        if not os.path.exists(json_filepath):
            raise RuntimeError(
                f"OpenAI credentials file doesn't exist: {json_filepath}"
            )

        with open(json_filepath) as f:
            data = json.load(f)
            self.organization = data["organization"]
            self.api_key = data["api_key"]
