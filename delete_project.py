sonarqube_host = "http://127.0.0.1:9000"
admin_token = "squ_062e0f933191285548d6966d82e09ebe37f7491a"
import requests


def delete_project(project_key: str):
    sonarqube_url = f"{sonarqube_host}/api/projects/delete"
    auth = (admin_token, "")
    response = requests.delete(sonarqube_url, auth=auth, data={"project": project_key})
    if response.ok:
        print(f"Project {project_key} deleted successfully.")
    else:
        print(
            f"Failed to delete project {project_key}. Status code: {response.status_code}, Response: {response.text}"
        )
