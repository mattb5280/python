import glob
import os
# Subdirectories
base_dir = "C:/tmp"
print("Subdirectories: ", glob.glob(f"{base_dir}/**/*",recursive=True))