import requests
import string
import random
import subprocess
import os
import datetime
import time
from pprint import pprint
from pprint import pformat
from typing import Any

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer

sonarqube_host = "http://127.0.0.1:9000"
sonarqube_url = f"{sonarqube_host}/api/projects/create"
admin_token = "squ_062e0f933191285548d6966d82e09ebe37f7491a"  # User Token


def create_project(project_name: str = "CPython"):
    project_key = f"project_key_{''.join([ random.choice(string.ascii_lowercase+string.digits) for _ in range(5)])}"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    project_data = {"name": project_name, "project": project_key}

    response = requests.post(
        sonarqube_url, headers=headers, data=project_data, auth=(admin_token, "")
    )

    if response.ok:
        print("Project created successfully.: name:", project_name, "key:", project_key)
    else:
        print(
            f"Failed to create project. Status code: {response.status_code}, Response: {response.text}"
        )
    return {"name": project_name, "key": project_key}


def clone_project(repo_url: str, project_name: str):
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    target_dir = f"./{project_name}"
    full_path_to_target_dir = os.path.join(current_file_directory, target_dir)
    if os.path.exists(full_path_to_target_dir):
        print(f"The directory {target_dir} already exists.")
        if os.path.exists(os.path.join(full_path_to_target_dir, ".git")):
            print(
                "The directory is already a git repository. Attempting to pull the latest changes."
            )
            try:
                subprocess.run(["git", "-C", target_dir, "pull"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to pull changes: {e}")
        else:
            print(
                "The directory is not a git repository. Consider removing it or choosing a different directory."
            )
    else:
        try:
            subprocess.run(["git", "clone", repo_url, target_dir], check=True)
            print(f"Repository cloned successfully into {target_dir}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone the repository: {e}")


def write_properties_file(
    local_project_name, project_name, project_key, target_dir, project_token
) -> None:
    with open(f"./{local_project_name}/sonar-project.properties", "w") as fd:
        fd.write(
            rf"""
sonar.projectKey={project_key}
sonar.projectName={project_name}
sonar.host.url={sonarqube_host}
sonar.token={project_token}
sonar.sources={target_dir}
            """
        )


def generate_project_token(project_key: str, project_name: str):
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
    expiration_date_str = expiration_date.strftime("%Y-%m-%d")
    sonarqube_url = f"{sonarqube_host}/api/user_tokens/generate"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "name": f"Analyse {project_name}{random.choice(string.ascii_lowercase+string.digits)}",
        "type": "PROJECT_ANALYSIS_TOKEN",
        "projectKey": project_key,
        "expirationDate": expiration_date_str,
    }
    response = requests.post(
        sonarqube_url, headers=headers, data=data, auth=(admin_token, "")
    )
    if response.ok:
        token = response.json().get("token")
        print(f"Generated Token for {project_key}: {token}")
        return token
    else:
        print(
            f"Failed to generate token for {project_key}. Status code: {response.status_code}, Response: {response.text}"
        )


def invoke_sonar_scanner(target_dir: str, project_key: str, project_token: str):
    # Change the current working directory to the project directory
    import os

    scanner_location = r"D:\sonar-scanner-cli-5.0.1.3006-windows\sonar-scanner-5.0.1.3006-windows\bin\sonar-scanner.bat"
    os.chdir(target_dir)
    build_command = rf"{scanner_location} -X -Dsonar.projectKey={project_key} -Dsonar.sources=. -Dsonar.host.url={sonarqube_host} -Dsonar.token={project_token}"
    try:
        subprocess.run(
            build_command,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to run sonar-scanner: {e}")
    except Exception as e:
        print(f"Failed to run sonar-scanner: {e}")


def pprint_color(obj: Any) -> None:
    """Pretty-print in color."""
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()), end="")


def retrieve_issues(project_key: str, use_pprint: bool = False):
    sonarqube_url = f"{sonarqube_host}/api/issues/search"
    auth = (admin_token, "")
    params = {
        "ps": 100,
        "s": "FILE_LINE",
        "components": project_key,
        "issueStatuses": "CONFIRMED,OPEN",  # For security issues, use impactSoftwareQualities=SECURITY
        "statuses": "OPEN",
    }
    response = requests.get(sonarqube_url, auth=auth, params=params)
    if response.ok:
        issues = response.json().get("issues", [])
        for issue in issues:
            # Process each issue as needed
            if use_pprint:
                pprint_color(issue)
            else:
                pprint(issue, indent=2)
    else:
        print(
            f"Failed to retrieve issues. Status code: {response.status_code}, Response: {response.text}"
        )


if __name__ == "__main__":
    project_name = "flask"
    project = create_project(project_name=project_name)
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    target_dir = rf"{current_file_directory}\flask"
    clone_project(repo_url="https://github.com/pallets/flask.git", project_name="flask")
    project_token = generate_project_token(project["key"], project["name"])
    invoke_sonar_scanner(target_dir, project["key"], project_token)
    time.sleep(10)
    retrieve_issues(project["key"])
