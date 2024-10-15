import requests
from requests.auth import HTTPBasicAuth

# Configuration
TENANT_ID = 'your-tenant-id'
CLIENT_ID = 'ea0616ba-638b-4df5-95b9-636659ae5121' # it is public and u can use it for every api method for Fabric
USERNAME = 'your-username'
PASSWORD = 'your-password'

# Get access token
def get_access_token(tenant_id, client_id, username, password):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "username": username,
        "password": password,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

# Get the list of workspaces
def get_workspaces(access_token):
    url = "https://api.powerbi.com/v1.0/myorg/groups"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])

# Get datasets in a workspace
def get_datasets(group_id, access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("value", [])

# Perform TakeOver on a dataset
def take_over_dataset(group_id, dataset_id, access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/Default.TakeOver"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(f"Take Over successfully completed for dataset: {dataset_id}")
    else:
        print(f"Error during Take Over: {response.status_code}, {response.text}")

# Main logic
def main():
    try:
        # Get access token
        access_token = get_access_token(TENANT_ID, CLIENT_ID, USERNAME, PASSWORD)
        print("Access token obtained.")

        # Get all workspaces
        workspaces = get_workspaces(access_token)
        print(f"Found {len(workspaces)} workspaces.")

        # Iterate through workspaces and perform TakeOver on all datasets
        for workspace in workspaces:
            group_id = workspace["id"]
            print(f"Processing workspace: {workspace['name']}")

            datasets = get_datasets(group_id, access_token)
            for dataset in datasets:
                dataset_id = dataset["id"]
                take_over_dataset(group_id, dataset_id, access_token)

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script
if __name__ == "__main__":
    main()
