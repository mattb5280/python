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
    try:
        ## Using curl:
        #  Works for a .zip download, but trying PDF download the return 
        #  file is HTML saying I'm being redirected to Sign On.
        cmd = f'curl --header "PRIVATE-TOKEN: E2vedJptnxfCshnCzaqe" --url "{elk_file_url}" --output "{copy_to_path}"'
        subprocess.run(cmd, check=True)

    except Exception as e:
        print(f'An error occurred: {e}')

def get_hash(url):
    
    git_cmd = f'git ls-remote {url}'
    ret = subprocess.run(git_cmd, capture_output=True, text=True)

    # ret_list = ret.stdout.split(" ",0)
    ret_list = ret.stdout.split()
    remote_git_hash = ret_list[0]

    return remote_git_hash

if __name__=='__main__':
    main()