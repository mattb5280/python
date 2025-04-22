import argparse
import os
import subprocess

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--elk_module_name", required=True, type=str)
    args = parser.parse_args()

    pull(args.elk_module_name)

def pull(elk_repo):
    """ 
        Git pull from Elk GitLab repository.
        Parameters:
        -----------
        elk_repo : str
                   Name of Elk module (ex: DAQ8 or RTX16) 
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

def copy_file(elk_file_url, copy_to_path):
    """
        Download file from Elk GitLab repository.
        Parameters:
        -----------
    """
    # Pull file from Elk repo
    import urllib.request
    try:
        urllib.request.urlretrieve(elk_file_url, copy_to_path)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__=='__main__':
    main()