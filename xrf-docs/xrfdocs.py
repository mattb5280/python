import os
import datetime
import glob
import logging
import shutil
import elkrepo

# Setup constants
XRF_FILES_DIR = ("C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - "
                 "Documents/XRF/Customer Pre-sales Support/Files")
XRF_COMMON_DIR = os.path.join(XRF_FILES_DIR,'common')
XRF_PROD_BRIEF_DIR = os.path.join(XRF_FILES_DIR, 'product_briefs')
LOG_FILE = os.path.join(XRF_FILES_DIR,'xrfdocs.log')

GITLAB_TOKEN='E2vedJptnxfCshnCzaqe'

xrf_dict = {"DAQ8": "XRF8",
            "RTX16": "XRF16"
            }

# Setup logging
if os.path.isfile(LOG_FILE):
    os.remove(LOG_FILE)

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logging.DEBUG)
logger.info(msg=f'Build Date = {datetime.datetime.now()}')

def main():
    """
    Facilitates the update of all XRF collateral packages
    """  
    hash = elkrepo.pull("Carriers")
    logger.info(msg=f'Elk Repo "Carrier" commit SHA: {hash}')

    hash = elkrepo.pull("DAQ8")
    logger.info(msg=f'Elk Repo "DAQ8" commit SHA: {hash}')

    hash = elkrepo.pull("RTX16")
    logger.info(msg=f'Elk Repo "RTX16" commit SHA: {hash}')

    hash = update_gsg()
    logger.info(msg=f'Elk Repo "Tutorial" commit SHA: {hash}')


    print('## Creating DeepDive Archives')
    fp = update_deepdive(eng_name='DAQ8')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)

    fp = update_deepdive(eng_name='RTX16')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)   

    print('## Creating TechPackage Archives')
    fp = update_tech_pkg(repo_name='DAQ8')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)
    cleanup(tmp_dir=fp)

    fp = update_tech_pkg(repo_name='RTX16')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)
    cleanup(tmp_dir=fp)

    print('## FINISHED!')
    print(f'## OUTPUT {XRF_FILES_DIR}')
    print(f'## LOG    {LOG_FILE}')

def update_pb(eng_name, dest_folder):
    """
    Copy latest Tria product briefs into dest folder
    
    Args:
        eng_name: str, Elk product name
        dest_folder: str, path to destination folder
    """
     # Create folder if missing
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Copy carrier and module product briefs
    pfx = xrf_dict[eng_name]
    src_pattern = os.path.join(XRF_PROD_BRIEF_DIR, f'*{pfx}*.pdf')

    for file_match in glob.glob(src_pattern):
        shutil.copy(file_match, dest_folder)

def update_gsg():
    """
    Copy latest Getting Started Guide from Elk repo into common folder
    """
    fn = 'Tria XRF Getting Started Guide.pdf'
    dest_filepath = os.path.join(XRF_COMMON_DIR,fn)

    hash = elkrepo.download_file(project_name='Tutorial', branch_name='master',
                          file_path='Getting_Started.pdf', output=dest_filepath)
    
    print(f'## Downloaded "{fn}" from remote.')
    
    return hash

def update_deepdive(eng_name):
    """
    Update archive of Overview files
    
    Args:
        eng_name: str, Elk product name
    """

    today = datetime.date.today()

    dest_folder = f'Tria_{xrf_dict[eng_name]}_DeepDive_{today.strftime("%Y%m%d")}'
    dest_path = os.path.join(XRF_FILES_DIR, dest_folder)

    update_pb(eng_name=eng_name,dest_folder=dest_path)

    # Copy latest Tria collateral common to all XRF products    
    pattern = ['*Quick Start*','*Getting Started*']

    shutil.copytree(XRF_COMMON_DIR, dest_path, dirs_exist_ok=True, 
                    ignore=shutil.ignore_patterns(*pattern))


    # Send manifest of all included file names to the log   
    logger.info(f'_____________________________________________')
    logger.info(f'TOP_FOLDER: {dest_folder}')
    logger.info(f'_____________________________________________')
    
    for files in os.listdir(dest_path):
        logger.info(f'ADDED: %s', files.removeprefix(XRF_FILES_DIR))

    return dest_path

def update_tech_pkg(repo_name):
    """
    Function to refresh XRF collateral from cloned repo.
    
    Args:
        repo_name: str, Name of Elk repo
    """
    # Create destination folder names
    if repo_name == 'DAQ8':
        pfx = 'XRF8'
        cc_repo_name = repo_name
        som_folder = f'{pfx} SOM (AES-XRF8-ZU47-G)'
        cc_folder  = f'{pfx} Carrier (AES-XRF8-CC-G)'

    elif repo_name == 'RTX16':
        pfx = 'XRF16'
        cc_repo_name = 'DAQ16'
        som_folder = f'{pfx} SOM (AES-XRF16-ZU49-G)'
        cc_folder  = f'{pfx} Carrier (AES-XRF16-CC-G-D)'
    else:
        som_folder = 'unknown_repo'


    # Create top-level archive name
    today = datetime.date.today()
    folder_name = f'Tria_{pfx}_TechPackage_{today.strftime("%Y%m%d")}'


    # Create staging folder
    tmp_dir = os.path.join('C:/tmp/',folder_name)
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    else:
        os.makedirs(tmp_dir)


    # Paths for SOM & CC staging folders
    som_dir = os.path.join(tmp_dir,som_folder)
    cc_dir = os.path.join(tmp_dir,cc_folder)


    # Copy SOM files from cloned Elk repo. Exclude binaries and restricted files.
    src_dir_som = f'C:/dev/elk/{repo_name}/Distribution/'
    pattern = ['*_SCH.PDF','*.txt','*.zip','.git','images','*.step','*.x_t','*.DWG','*.md']
    shutil.copytree(src_dir_som, som_dir, ignore=shutil.ignore_patterns(*pattern))


    # Copy CC files from cloned Elk repo. Exclude binaries and restricted files.
    src_dir_cc = f'C:/dev/elk/Carriers/distribution/{cc_repo_name}'
    pattern = ['PCB','RF Shield','.git*','*.md','*.step','*.x_t','*.DWG','*.DXF','*.scc','SEAF8*']
    shutil.copytree(src_dir_cc, cc_dir, ignore=shutil.ignore_patterns(*pattern))


    # Copy latest Tria collateral common to all XRF products
    shutil.copytree(XRF_COMMON_DIR, tmp_dir, dirs_exist_ok=True)


    # Copy latest Tria product briefs for this XRF version
    update_pb(repo_name, tmp_dir)


    # Descend all dirs and remove empty folders
    rm_empty_dir(tmp_dir)


   # Send manifest of all included file names to the log
    logger.info(f'_____________________________________________')
    logger.info(f'TOP_FOLDER: {folder_name}')
    logger.info(f'_____________________________________________')

    for inc_files in glob.glob(f'{tmp_dir}/**/*', recursive=True):
        logger.info(f'ADDED: %s', inc_files.removeprefix(tmp_dir))

    return tmp_dir


def rm_empty_dir(root, preserve=True):
    """
    Function to remove empty folders.

    Args:
        root: str, path to starting folder
        preserve: bool, default=true, do we keep the root folder itself?
    """
    for path in (os.path.join(root, p) for p in os.listdir(root)):
        if os.path.isdir(path):
            rm_empty_dir(path, preserve=False)
    if not preserve:
        try:
            os.rmdir(root) # only removes empty dirs
        except IOError:
            pass


def make_zip(src_folder,dest_folder):
    """
    Function to zip staged archive and move to destination folder.

    Args:
        src_folder: str, path to folder that will be zipped
        dest_folder: str, folder where zip file will be moved to
    """
    output_file = src_folder
    shutil.make_archive(output_file,'zip',src_folder)

    path, folder_name = os.path.split(src_folder)
    archive_name = f'{folder_name}.zip'
    
    dest_path = os.path.join(dest_folder,archive_name)
    shutil.move(f'{output_file}.zip', f'{dest_path}')

    msg = f'ZIPPED: {dest_path}'
    # print(msg)
    logger.info(msg)

def cleanup(tmp_dir):
    """
    Function to clean up temporary build artifacts

    Args:
        tmp_dir: str, path to folder that will be deleted
    """
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    
if __name__=='__main__':
    logger.info('Generated by: mattb5280/python/xrf-docs/xrfdocs.py')
    main()

else:
    logger.info(f'Generated by: {__name__}')
