from PIL import Image
import argparse, os
import glob

### How to use this script on Windows:
### First: cd {dir of python script} 
### Secondly: python FileConverter.py --path {path_to_folder} --folder {folder to convert} --findformat {.tif for example} --convertto{.png for example}

# STARTFORMAT = ".tif"
# NEWFORMAT = ".png"

parser = argparse.ArgumentParser(description='Segment images in folder.')
parser.add_argument('--path', required=True)
parser.add_argument('--folder', required=True)
parser.add_argument('--findformat', required=True)
parser.add_argument('--convertto', required=True)
args = parser.parse_args()

STARTFORMAT = args.findformat
NEWFORMAT = args.convertto

os.chdir(args.path) #change dir to new root dir
if not os.path.isdir(args.folder+"_"+NEWFORMAT):
    os.mkdir(args.folder+"_"+NEWFORMAT)
    print(f"Main folder {args.folder+'_'+NEWFORMAT} has been created")
else:
    print("Main folder already exists")

folders_to_check = [os.path.join(args.folder, folder) for folder in os.listdir(args.folder)]

def change_root(folder, root):
    split_path = folder.split("\\")
    start = split_path[0].replace(root, root+"_"+NEWFORMAT)
    return os.path.join(start, "\\".join(split_path[1:]))

while len(folders_to_check) > 0:
    folder_to_check = folders_to_check[0]

    ## Add to check folder into new _+NEWFORMAT folder
    new_to_check_folder =  change_root(folder_to_check, args.folder)
    if not os.path.isdir(new_to_check_folder): #check if folder already exists
        os.mkdir(new_to_check_folder)
        print(f"{new_to_check_folder} has been created") 

    ##check for images and convert
    images = glob.glob(os.path.join(folder_to_check, f"*{STARTFORMAT}"))
    for image in images: #convert images
        img_ = Image.open(image)
        image = change_root(image, args.folder)
        image = image.replace(STARTFORMAT, NEWFORMAT)
        img_.save(image)
    if len(images) > 0:
        print(f"Converted {len(images)} images in {folder_to_check} from {STARTFORMAT} to {NEWFORMAT}")

    ##check for subfolders
    new_folders = os.listdir(folder_to_check)
    for folder in new_folders:
        folder_path = os.path.join(folder_to_check, folder)
        if os.path.isdir(folder_path):
            folders_to_check.append(folder_path) # add subfolders to check list
      
    ## remove folder from list
    folders_to_check.remove(folder_to_check)

print(f"Finished converting all {STARTFORMAT} files to {NEWFORMAT} in directory {args.folder}")