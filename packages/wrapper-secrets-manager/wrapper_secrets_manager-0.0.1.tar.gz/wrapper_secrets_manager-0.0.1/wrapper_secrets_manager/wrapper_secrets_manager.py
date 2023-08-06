import google.cloud.secretmanager as sm


class GoogleSecretsWrapper:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = sm.SecretManagerServiceClient()

    def get_secret(self, secret_name):
        secret_path = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = self.client.access_secret_version(request={"name": secret_path})
        return response.payload.data.decode("UTF-8")
