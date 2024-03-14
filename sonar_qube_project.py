import requests
import string
import random
import subprocess
import os

sonarqube_host = "http://127.0.0.1:9000"
sonarqube_url = f"{sonarqube_host}/api/projects/create"
admin_token = "squ_062e0f933191285548d6966d82e09ebe37f7491a"  # User Token


def create_project():
    project_key = f"project_key_{''.join([ random.choice(string.ascii_lowercase+string.digits) for _ in range(5)])}"
    project_name = "CPython"

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


def clone_project():
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    repo_url = "https://github.com/pallets/flask.git"
    project_name = "flask"
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


def write_properties_file(project_name, project_key) -> None:
    with open(f"./{project_name}/sonar-project.properties", "w") as fd:
        fd.write(
            f"""
                sonar.projectKey={project_key}
                sonar.projectName={project_name}
                sonar.sources=.
            """
        )


def invoke_sonar_scanner(target_dir: str):
    # Change the current working directory to the project directory
    import os
    os.chdir(target_dir)
    subprocess.run(["sonar-scanner"], check=True)


def retrieve_issues(project_key: str):
    sonarqube_url = f"{sonarqube_host}/api/issues/search"
    headers = {"Authorization": f"Basic {admin_token}"}
    params = {"projects": project_key, "statuses": "OPEN"}
    response = requests.get(sonarqube_url, headers=headers, params=params)
    if response.ok:
        issues = response.json().get("issues", [])
        for issue in issues:
            # Process each issue as needed
            print(issue)
    else:
        print(
            f"Failed to retrieve issues. Status code: {response.status_code}, Response: {response.text}"
        )


if __name__ == "__main__":
    project = create_project()
    clone_project()
    write_properties_file(project["name"], project["key"])
    invoke_sonar_scanner("flask")
    retrieve_issues(project["key"])
