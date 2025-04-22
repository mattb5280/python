import os, datetime, glob, logging
import shutil

import elk_repo

def main():
    # Get latest files from cloned repos
    elk_repo.pull("Carriers")
    elk_repo.pull("DAQ8")
    elk_repo.pull("RTX16")
        
    fp = update_files("DAQ8")
    print(f'Copied DAQ8 files to: {fp}')
    make_zip(fp)

    fp = update_files("RTX16")
    print(f'Copied RTX16 files to: {fp}')
    make_zip(fp)

# Function to refresh XRF collateral from cloned repo
def update_files(repo_name):
    # Set product strings according to module engineering name
    if repo_name == "DAQ8":
        pfx = 'XRF8'
        cc_repo_name = repo_name
        som_folder = f'{pfx} SOM (AES-XRF8-ZU47-G)'
        cc_folder = f'{pfx} Carrier (AES-XRF8-CC-G)'

    elif repo_name == "RTX16":
        pfx = 'XRF16'
        cc_repo_name = "DAQ16"
        som_folder = f'{pfx} SOM (AES-XRF16-ZU49-G)'
        cc_folder = f'{pfx} Carrier (AES-XRF16-CC-G-D)'
    else:
        som_folder = f'unknown_repo'

    # Create top-level archive name
    today = datetime.date.today()
    folder_name = f'Tria_{pfx}_Tech_Package_{today.strftime("%Y%m%d")}'

    # Create staging folder
    tmp_dir = os.path.join('C:/tmp/',folder_name)
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    else:
        os.makedirs(tmp_dir)

    # Setup stage paths for SOM & CC folders
    som_dir = os.path.join(tmp_dir,som_folder)
    cc_dir = os.path.join(tmp_dir,cc_folder)

    # SOM: Copy from cloned Elk repo - exclude binaries and restricted files.
    src_dir_som = f'C:/dev/elk/{repo_name}/Distribution/'
    pattern = ['*_SCH.PDF','*.txt','*.zip','.git','images','*.step','*.x_t','*.DWG','*.md']
    shutil.copytree(src_dir_som, som_dir, ignore=shutil.ignore_patterns(*pattern))

    # CARRIER: Copy from cloned Elk repo - exclude binaries and restricted files.
    src_dir_cc = f'C:/dev/elk/Carriers/distribution/{cc_repo_name}'
    pattern = ['PCB','RF Shield','.git*','*.md','*.step','*.x_t','*.DWG','*.DXF','*.scc','SEAF8*']
    shutil.copytree(src_dir_cc, cc_dir, ignore=shutil.ignore_patterns(*pattern))

    # MISC: Copy latest Tria collateral common to all XRF products
    base_dir = "C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - Documents/XRF/Customer Support/Files"
    common_dir = os.path.join(base_dir, 'common')
    shutil.copytree(common_dir, tmp_dir, dirs_exist_ok=True)

    # Copy GSG file from Elk tutorial repo (too large to clone)
    gsg_path = os.path.join(common_dir, "Tria XRF Getting Started Guide.pdf")
    elk_repo.copy_file(
        "https://gitlab.elkengineering.net/common/tutorial/-/blob/master/Getting_Started.pdf",
        gsg_path
        )

    # MISC: Copy latest Tria product briefs for this XRF version
    pb_dir = os.path.join(base_dir, 'product_briefs')
    file_pattern = f'*{pfx}*.pdf'
    src_pattern = os.path.join(pb_dir, file_pattern)

    for file_match in glob.glob(src_pattern):
        shutil.copy(file_match, tmp_dir)
        # print(f'Copied: {file_match}')

    rm_empty_dir(tmp_dir)

    # Setup logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='xrf-docs.log', encoding='utf-8', level=logging.DEBUG)

    for inc_files in glob.glob(f'{tmp_dir}/**/*', recursive=True):
    #    print("Included file: %s", inc_files )
        logger.info(f'Included file: %s', inc_files)

    return tmp_dir

# Function to remove empty folders
def rm_empty_dir(root, preserve=True):
    for path in (os.path.join(root, p) for p in os.listdir(root)):
        if os.path.isdir(path):
            rm_empty_dir(path, preserve=False)
    if not preserve:
        try:
            os.rmdir(root) # only removes empty dirs
        except IOError:
            pass

# Function to zip staged archive and move to destination folder
def make_zip(folderpath):
    print(f'zipping file: {folderpath} ...')

    output_file = folderpath
    shutil.make_archive(output_file,'zip',folderpath)

    path, folder_name = os.path.split(folderpath)
    archive_name = f'{folder_name}.zip'
    
    dest_path= os.path.join(
        "C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - Documents/XRF/Customer Support/Files",
        archive_name
        )
    shutil.move(f'{output_file}.zip', f'{dest_path}')

    print(f'zip archive posted to: {dest_path}')

def cleanup(tmp_dir):
    print('Please cleanup after yourself')

    
if __name__=='__main__':
    main()


