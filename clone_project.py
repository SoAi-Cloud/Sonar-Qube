import subprocess

# The URL of the repository you want to clone
repo_url = "https://github.com/pallets/flask.git"
# The directory where you want to clone the repository
project_name = "flask"
target_dir = f"./{project_name}"

# Clone the repository
subprocess.run(["git", "clone", repo_url, target_dir], check=True)

sonar.projectKey=your_project_key
sonar.projectName=Your Project Name
sonar.sources=src
