import requests

sonarqube_url = "http://127.0.0.1:9000"
admin_username = "admin"
admin_password = "srinivas@123"
project_key = "your_new_project_key"

response = requests.get(
    f"{sonarqube_url}/api/issues/search",
    auth=(admin_username, admin_password),
    params={"projectKeys": project_key},
)

if response.ok:
    issues = response.json()
    print("Analysis Issues:", issues)
else:
    print("Failed to retrieve issues. Response Code:", response.status_code)
