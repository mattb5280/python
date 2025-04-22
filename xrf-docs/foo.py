import os
import shutil
import elk_repo    

# MISC: Copy latest Tria collateral common to all XRF products
base_dir = "C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - Documents/XRF/Customer Support/Files"
common_dir = os.path.join(base_dir, 'common')


# Pull file from Elk : Tutorial repo

# import urllib.request
gsg_path = os.path.join(common_dir, "__Tria XRF Getting Started Guide.pdf")
# urllib.request.urlretrieve("https://gitlab.elkengineering.net/common/tutorial/-/blob/master/Getting_Started.pdf", gsg_path)
try:
    elk_repo.copy_elk_file(
        "https://gitlab.elkengineering.net/common/tutorial/-/blob/master/Getting_Started.pdf",
        gsg_path)
except Exception as e:
    print(f'An error occurred: {e}')