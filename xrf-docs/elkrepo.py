import argparse
import os
import subprocess
import gitlab

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--elk_module_name", required=True, type=str)
    args = parser.parse_args()

    pull(args.elk_module_name)

def pull(elk_repo):
    """ 
    Git pull from Elk GitLab repository.
    
    Args:
        elk_repo: str, Name of Elk module (ex: DAQ8 or RTX16) 
    """
    local_dir = os.path.join("C:\\dev\\elk\\",elk_repo,"Distribution")

    print(f'Pulling remote to {local_dir} ...')

    # Use subprocess to run git command.
    # (GitPython library was having problems doing the same)
    try:
        git_cmd = f'pushd "{local_dir}" && git pull && popd'
        ret = subprocess.call(git_cmd, shell=True)
    except Exception as e:
        print(f"An error occurred: {e}")


def download_file(host, token, project_name, branch_name, file_path, output):
    """
    Download single-file from GitLab repo using python-gitlab

    Args:
        host: str, gitlab URL domain only, without project/path
        project_name: str, GitLab project name
        branch_name: str, GitLab branch name
        file_path: str, GitLab path to desired file
        output: str, Local storage file path
    """
    try:
        gl = gitlab.Gitlab(host, private_token=token)
        pl = gl.projects.list(search=project_name)
        for p in pl:
            if p.name == project_name:
                project = p
                break
        with open(output, 'wb') as f:
            project.files.raw(file_path=file_path, ref=branch_name, streamed=True, action=f.write)

    except Exception as e:
        print("Error:", e)


def get_hash(url):
    """
    Request latest git hash from the HEAD of a remote
    
    Args:
        url: str, URL of GitLab repo
    """
    
    git_cmd = f'git ls-remote {url}'
    ret = subprocess.run(git_cmd, capture_output=True, text=True)

    ret_list = ret.stdout.split()
    remote_git_hash = ret_list[0]

    return remote_git_hash

if __name__=='__main__':
    main()