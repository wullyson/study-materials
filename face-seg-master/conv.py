from os import listdir, makedirs
from os.path import isfile, join, exists
import shutil

def getAllFileInFolder(folderPath, fileExtension):
    totalExtension = ''
    if fileExtension.startswith('.'):
        totalExtension = fileExtension
    else:
        totalExtension = '.' + fileExtension

    return [f for f in listdir(folderPath) if isfile(join(folderPath, f)) and f.endswith(totalExtension)]


def getAllFoldersInFolder(folderPath):
    return [f for f in listdir(folderPath) if not isfile(join(folderPath, f))]


# Start
if True: #__name__ == '__main__':
    dataset_folder = 'lfw_funneled'
    # get all folder names
    folders = getAllFoldersInFolder(dataset_folder)
    # get all file names
    image_path = []
    image_name = []
    for folder in folders:
        subfolder_path = join(dataset_folder, folder)
        files = getAllFileInFolder(subfolder_path, 'jpg')
        for f in files:
            image_path.append(subfolder_path)
            image_name.append(f)

    # Generate the new folder structure
    new_folder_path = 'raw'
    if exists(new_folder_path):
        shutil.rmtree(new_folder_path)

    dst_path = join(new_folder_path, 'images')
    makedirs(dst_path)
    # copy all the images
    for src_path, src_image in zip(image_path, image_name):
        src = join(src_path, src_image)
        dst = join(dst_path, src_image)
        shutil.copyfile(src, dst)

    print("Job finished")
