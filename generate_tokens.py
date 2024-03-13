import requests

sonarqube_url = "http://your.sonarqube.server"
admin_username = "your_admin_username"
admin_password = "your_admin_password"
token_name = "your_desired_token_name"

response = requests.post(
    f"{sonarqube_url}/api/user_tokens/generate",
    auth=(admin_username, admin_password),
    data={"name": token_name}
)

if response.ok:
    token = response.json().get('token')
    print("Generated Token:", token)
else:
    print("Failed to generate token. Response Code:", response.status_code)
