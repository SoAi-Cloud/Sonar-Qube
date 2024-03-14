import requests

sonarqube_url = "http://127.0.0.1:9000"
admin_username = "admin"
admin_password = "srinivas@123"
token_name = "CPython1"

response = requests.post(
    f"{sonarqube_url}/api/user_tokens/generate",
    auth=(admin_username, admin_password),
    data={"name": token_name},
)
breakpoint()
if response.ok:
    token = response.json().get("token")
    print("Generated Token:", token)
else:
    print("Failed to generate token. Response Code:", response.status_code)
