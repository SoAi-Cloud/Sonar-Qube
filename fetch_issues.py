import requests

# Configuration
sonarqube_url = "http://127.0.0.1:9000"
admin_username = "admin"
admin_password = "srinivas@123"
auth_token = (
    "squ_00ab0dbc74c5849b60d76097f79b1986bb1194a2"  # Replace with your SonarQube token
)
project_key = "CPython"  # Replace with your SonarQube project key

# Headers for authentication
headers = {"Authorization": f"Basic {auth_token}"}

# Parameters for the API request
params = {"componentKeys": project_key}  # Identifies the project to fetch issues for

# API endpoint for fetching issues
issues_api_url = f"{sonarqube_url}/api/issues/search"

# Making the GET request
response = requests.get(issues_api_url, headers=headers, params=params)

# Checking if the request was successful
if response.ok:
    # Parse the JSON response
    issues_data = response.json()
    issues = issues_data.get("issues", [])

    # Print out the issues
    for issue in issues:
        print(
            f"Issue: {issue.get('message')} at {issue.get('component')}, Line: {issue.get('line')}"
        )
else:
    print(
        f"Failed to fetch issues. Status Code: {response.status_code}, Response: {response.text}"
    )
