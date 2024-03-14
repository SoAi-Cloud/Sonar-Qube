import requests
import string
import random

sonarqube_host = "http://127.0.0.1:9000"


sonarqube_url = f"{sonarqube_host}/api/projects/create"
admin_token = "squ_062e0f933191285548d6966d82e09ebe37f7491a"  # User Token

project_key = f"project_key_{''.join([ random.choice(string.ascii_lowercase+string.digits) for _ in range(5)])}"
project_name = "CPython"

headers = {"Content-Type": "application/x-www-form-urlencoded"}

project_data = {"name": project_name, "project": project_key}

response = requests.post(
    sonarqube_url, headers=headers, data=project_data, auth=(admin_token, "")
)

if response.ok:
    print("Project created successfully.")
else:
    print(
        f"Failed to create project. Status code: {response.status_code}, Response: {response.text}"
    )
