# import xrfdocs as dut
import os,shutil,glob
import elkrepo
# import xrfdocs

XRF_FILES_DIR = ("C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - "
                 "Documents/XRF/Customer Pre-sales Support/Files")
XRF_COMMON_DIR = os.path.join(XRF_FILES_DIR,'common')
XRF_PROD_BRIEF_DIR = os.path.join(XRF_FILES_DIR, 'product_briefs')
LOG_FILE = os.path.join(XRF_FILES_DIR,'xrfdocs.log')

# # dut.update_pb("DAQ8", dut.xrf8_rfi_folder)
# # dut.update_pb("RTX16", dut.xrf16_rfi_folder)

# dut.update_overview("DAQ8")

# import xrfdocs as dut
# fp = dut.update_overview(eng_name="DAQ8")
# fp = dut.update_overview(eng_name="RTX16")

tutorial_remote = 'git@gitlab.elkengineering.net:common/tutorial.git'
remote_hash = elkrepo.get_hash(tutorial_remote)
pattern = os.path.join(XRF_COMMON_DIR,"*Getting*Started*")

# for file_match in glob.glob(pattern):
#     fn = file_match.rstrip("pdf").rstrip(".")
file_match = glob.glob(pattern)

if len(file_match) > 1:
    msg = f'WARNING: multiple copies of GETTING STARTED GUIDE found in {XRF_COMMON_DIR}'
    print(msg)

# for x in file_match:
#     hash_match = remote_hash[0:8] in x

# hash_match = any(remote_hash[0:8] in x for x in file_match)

if not any(remote_hash[0:8] in x for x in file_match):
    msg = f'WARNING: NOT current with hash {remote_hash}'
    print(msg)
else:
    print('HASH MATCH FOUND')
    
    # if not remote_hash[0:8] in fn:
# if not remote_hash[0:8] in (glob.glob(pattern)):
    # msg = f'NOTICE: {fn} is current with hash {remote_hash}'
    # logger.info(msg)
# else:
    # msg = f'WARNING: {fn} is NOT current with hash {remote_hash}'
    # print(msg)
