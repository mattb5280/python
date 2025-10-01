import argparse
import os
import subprocess
import gitlab
import git

HOST_URL = 'https://gitlab.elkengineering.net/'
TOKEN_FILE = 'C:/Users/027419/OneDrive - Avnet/Documents/Avnet_Git/GitLab/py-read-token-elkrepo.txt'

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--elk_prod_name", required=True, type=str)
    args = parser.parse_args()

    pull(args.elk_prod_name)

def pull(elk_prod_name):
    """ 
    Git pull from Elk GitLab repository.
    
    Args:
        elk_prod_name: str, Name of Elk module (ex: DAQ8 or RTX16) 
    """
    local_dir = os.path.join("C:\\dev\\elk\\",elk_prod_name,"Distribution")

    print(f'## Pulling remote to {local_dir} ...')

    # Use subprocess to run git pull
    # (GitPython library was having problems doing the same)
    try:
        git_cmd = f'pushd "{local_dir}" && git pull && popd'
        ret = subprocess.call(git_cmd, shell=True)
    except Exception as e:
        print(f"An error occurred: {e}")

    # hash = get_hash(elk_prod_name + "/Distribution")
    

    # try:
    # # Initialize the Repo object
    #     repo = git.Repo(local_dir)

    #     # Get the 'origin' remote (or any other remote you want to pull from)
    #     origin = repo.remotes.origin

    #     # Perform the pull operation
    #     # This fetches changes from the remote and merges them into the current branch
    #     origin.pull()

    #     print(f"Successfully pulled changes from {origin.name} into {repo_path}")

    # except git.InvalidGitRepositoryError:
    #     print(f"Error: '{local_dir}' is not a valid Git repository.")
    # except Exception as e:
    #     print(f"An error occurred during the pull operation: {e}")

    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def download_file(project_name, branch_name, file_path, output):
    """
    Download single-file from GitLab repo using python-gitlab

    Args:
        project_name: str, GitLab project name
        branch_name: str, GitLab branch name
        file_path: str, GitLab path to desired file
        output: str, Local storage file path
    """

    try:
        gl = gitlab.Gitlab(HOST_URL, private_token=get_token())
        pl = gl.projects.list(search=project_name)
        for p in pl:
            if p.name == project_name:
                project = p
                break
        with open(output, 'wb') as f:
            project.files.raw(file_path=file_path, ref=branch_name, streamed=True, action=f.write)

    except Exception as e:
        print("Error:", e)

    commit = p.commits.get('master')
    
    return commit.id

def get_hash(project_path):
    """
    Request latest git hash from the HEAD of a remote
    
    Args:
        elk_prod_name: str, Elk product name
    """   
    
    # project_path = elk_prod_name.lower() + "/Distribution"

    try:
        gl = gitlab.Gitlab(HOST_URL, private_token=get_token())
        pl = gl.projects.get(project_path)
        commit = pl.commits.get('master')

    except Exception as e:
        print("Error:", e)

    return commit.id

def get_token():
    """Get GitLab token from local file
    """
    try:
        with open(TOKEN_FILE, "r") as file:
            token = file.read().strip()
    except FileNotFoundError:
        print("Error: The file 'your_file.txt' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return token

if __name__=='__main__':
    main()