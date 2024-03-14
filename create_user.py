import requests

sonarqube_url = "http://127.0.0.1:9000/api/users/create"
admin_token = "squ_062e0f933191285548d6966d82e09ebe37f7491a"  # User Token

headers = {"Content-Type": "application/x-www-form-urlencoded"}
user_data = {
    "login": "new_username",
    "password": "new_password",
    "name": "Srinivas Reddy Thatiparthy",
    "email": "thatiparthysreenivas@gmail.com",
}

response = requests.post(
    sonarqube_url, headers=headers, data=user_data, auth=(admin_token, "")
)

if response.status_code == 200:
    print("User created successfully.")
else:
    print(
        f"Failed to create user. Status code: {response.status_code}, Response: {response.text}"
    )
