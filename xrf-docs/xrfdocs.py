import os
import datetime
import glob
import logging
import shutil
import webbrowser
import elkrepo

XRF_FILES_DIR = ("C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - "
                 "Documents/XRF/Customer Support/Files")
XRF_COMMON_DIR = os.path.join(XRF_FILES_DIR,'common')
XRF_PROD_BRIEF_DIR = os.path.join(XRF_FILES_DIR, 'product_briefs')
LOG_FILE = os.path.join(XRF_FILES_DIR,'xrfdocs.log')

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
    """Executive function that sequences the update
    """
    elkrepo.pull("Carriers")
    elkrepo.pull("DAQ8")
    elkrepo.pull("RTX16")

    # Update 'Overview' files and zip
    fp = update_deepdive(eng_name='DAQ8')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)

    fp = update_deepdive(eng_name='RTX16')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)   
        
    # Update 'Tech Package' files and zip
    fp = update_tech_pkg(repo_name='DAQ8')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)
    cleanup(tmp_dir=fp)

    fp = update_tech_pkg(repo_name='RTX16')
    make_zip(src_folder=fp, dest_folder=XRF_FILES_DIR)
    cleanup(tmp_dir=fp)

def update_pb(eng_name, dest_folder):
    """Copy latest Tria product briefs into dest folder

    Keyword arguments:
    eng_name -- Elk product name
    dest_folder -- path to destination folder
    """
    pfx = xrf_dict[eng_name]
    src_pattern = os.path.join(XRF_PROD_BRIEF_DIR, f'*{pfx}*.pdf')

    # Create folder if missing
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Copy all that match pattern
    for file_match in glob.glob(src_pattern):
        shutil.copy(file_match, dest_folder)

def update_deepdive(eng_name):
    """Update archive of Overview files

    Keyword arguments:
    eng_name -- Elk product name
    """
    today = datetime.date.today()

    dest_folder = f'Tria_{xrf_dict[eng_name]}_DeepDive_{today.strftime("%Y%m%d")}'
    dest_path = os.path.join(XRF_FILES_DIR, dest_folder)

    logger.info(f'_____________________________________________')
    logger.info(f'TOP_FOLDER: {dest_folder}')
    logger.info(f'_____________________________________________')

    update_pb(eng_name=eng_name,dest_folder=dest_path)

    # Copy latest Tria collateral common to all XRF products    
    pattern = ['*Quick Start*','*Getting Started*']

    shutil.copytree(XRF_COMMON_DIR, dest_path, dirs_exist_ok=True, 
                    ignore=shutil.ignore_patterns(*pattern))
    
    for files in os.listdir(dest_path):
        logger.info(f'ADDED: %s', files.removeprefix(XRF_FILES_DIR))

    return dest_path

def update_tech_pkg(repo_name):
    """Function to refresh XRF collateral from cloned repo.

    Parameters
    ----------
    repo_name : string

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

    logger.info(f'_____________________________________________')
    logger.info(f'TOP_FOLDER: {folder_name}')
    logger.info(f'_____________________________________________')

    # Send manifest of all included file names to the log
    for inc_files in glob.glob(f'{tmp_dir}/**/*', recursive=True):
        logger.info(f'ADDED: %s', inc_files.removeprefix(tmp_dir))

    # Check for updates of GSG file in Elk tutorial repo, which is too large to 
    # clone everytime. Unable to successfully download single PDF from python.
    # So we compair the remote hash to the 8-digit suffix in the local filename
    # and open the file URL in a browser if they do not match.
    tutorial_remote = 'git@gitlab.elkengineering.net:common/tutorial.git'
    remote_hash = elkrepo.get_hash(tutorial_remote)
    pattern = os.path.join(XRF_COMMON_DIR,"*Getting*Started*")
    
    for file_match in glob.glob(pattern):
        fn = os.path.basename(file_match.rstrip(".pdf"))
    
    if remote_hash[0:8] in fn:
        msg = f'NOTICE: {fn} is current with hash {remote_hash}'
        logger.info(msg)
    else:
        msg = f'WARNING: {fn} is NOT current with hash {remote_hash}'
        logger.warning(msg)
        print(msg)

        elk_gsg_url = ('https://gitlab.elkengineering.net/common/tutorial/-'
                       '/raw/master/Getting_Started.pdf?inline=false')
        webbrowser.open(elk_gsg_url, autoraise=True,)
        
    print(msg)      

    return tmp_dir


def rm_empty_dir(root, preserve=True):
    """Function to remove empty folders.

    Keyword args:
    root -- path to starting folder
    preserve -- do we keep the root folder itself? (logical)
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
    """Function to zip staged archive and move to destination folder.

    Keyword args:
    src_folder -- path to folder that will be zipped
    dest_folder -- folder where zip file will be moved to
    """
    output_file = src_folder
    shutil.make_archive(output_file,'zip',src_folder)

    path, folder_name = os.path.split(src_folder)
    archive_name = f'{folder_name}.zip'
    
    dest_path = os.path.join(dest_folder,archive_name)
    shutil.move(f'{output_file}.zip', f'{dest_path}')

    msg = f'ZIPPED: {dest_path}'
    print(msg)
    logger.info(msg)

def cleanup(tmp_dir):
    """Function to clean up temporary build artifacts
    """
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    
if __name__=='__main__':
    logger.info('Generated by: mattb5280/python/xrf-docs/xrfdocs.py')
    main()

else:
    logger.info(f'Generated by: {__name__}')
