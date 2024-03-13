import requests

sonarqube_url = "http://127.0.0.1:9000"
admin_username = "admin"
admin_password = "srinivas@123"
token_name = "CPython"
project_key = "your_new_project_key"
project_name = "CPython"

response = requests.post(
    f"{sonarqube_url}/api/projects/create",
    auth=(admin_username, admin_password),
    data={"name": project_name, "project": project_key}
)

if response.ok:
    print(f"Project '{project_name}' created successfully.")
else:
    print("Failed to create project. Response Code:", response.status_code)
