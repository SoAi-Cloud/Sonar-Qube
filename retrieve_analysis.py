import requests

response = requests.get(
    f"{sonarqube_url}/api/issues/search",
    auth=(admin_username, admin_password),
    params={"projectKeys": project_key}
)

if response.ok:
    issues = response.json()
    print("Analysis Issues:", issues)
else:
    print("Failed to retrieve issues. Response Code:", response.status_code)
