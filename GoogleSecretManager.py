from google.cloud import secretmanager
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ferna/Desktop/PruebaData/Credentials/massive-woods-393817-a54a8a2313e4.json"

class GoogleSecretsManager:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret_value(self, secret_name):
        # Build the secret name using the project ID and the provided secret name
        secret_path = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"

        try:
            # Access the secret version
            response = self.client.access_secret_version(name=secret_path)
            secret_value = response.payload.data.decode("UTF-8")
            return secret_value
        except Exception as e:
            print(f"Error retrieving secret '{secret_name}': {e}")
            return None
