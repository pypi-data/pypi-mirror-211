import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError

def load_secret(secret_name):
    dashed_name = secret_name.replace("-", "_")
    ev = os.getenv(dashed_name)
    if ev:
        return ev
    
    credential = DefaultAzureCredential()
    key_vault_uri = os.getenv("KEY_VAULT_URI")
    if not key_vault_uri:
        raise Exception("Enviromental Variable KEY_VAULT_URI missing.")
    
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    try:
        secret_value = client.get_secret(secret_name).value
        return secret_value
    except ResourceNotFoundError:
        raise ValueError(f"Secret '{secret_name}' not found in Azure Key Vault.")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve secret '{secret_name}' from Azure Key Vault: {str(e)}")
