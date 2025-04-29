import os

XRF_FILES_DIR = ("C:/Users/027419/Avnet/Engineering & Technology 5G-DSP - "
                "Documents/XRF/Customer Support/Files")

def main():
    root_level = 0
    path, root_folder = os.path.split(XRF_FILES_DIR)
    print(f'ROOT: {XRF_FILES_DIR}')
    print(f'[{root_level}]{root_folder}/')

    find_empty_dirs(root=XRF_FILES_DIR, level=root_level)

def find_empty_dirs(root, level):
    # Flag empty DIRS:
    for path in (os.path.join(root, p) for p in os.listdir(root)):

        if os.path.isdir(path):
            # if len(os.listdir(path)) == 0:
                # print(f'## EMPTY ({level}): {path}')
            # else:

            base_path, root_folder = os.path.split(path)

            if len(os.listdir(path)) == 0:
                file_str = f'{root_folder}/ [EMPTY_FOLDER]'
            else:
                file_str = f'{root_folder}/'

            next_level = level + 1

            msg = f'[{next_level}]:' + make_space(next_level) + f'{file_str}' 
            print(msg)
            find_empty_dirs(root=path,level=next_level)

def make_space(level):
    
    indent = "   "
    space_str = ""
    pfx = "├─ "
    for spaces in range(level):
        space_str = space_str + indent
    
    level_string = space_str + pfx

    return level_string

if __name__=='__main__':
    main()