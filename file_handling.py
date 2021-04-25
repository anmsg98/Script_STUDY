import os
import shutil
import random

ext_list = [
    'doc', 'ppt', 'py', 'pdf', 'hwp',
    'txt', 'cpp', 'h', 'htm', 'mov',
    'mp4', 'avi', 'dll', 'jpg', 'png',
    'tmp', 'zip', 'bin', 'bat', 'gif'
]

total_num_folders = 0

def make_subfolders(limit):
    global total_num_folders

    subfolders = []
    for i in range(3):
        path = 'folder%03d' % total_num_folders
        subfolders.append(path)
        print('create folder : ' + path)
        os.mkdir(path)
        total_num_folders += 1
        if total_num_folders > limit:
            return

    random.shuffle(subfolders)
    for folder in subfolders:
        os.chdir(folder)

        random_files = ['file%d.%s' % (i, ext_list[random.randint(0, len(ext_list) - 1)]) for i in range(10)]
        for fn in random_files:
            f = open(fn, 'w')
            f.write('Randomly Generated File')
            f.close()

        make_subfolders(limit - 3)
        os.chdir('..')



def make_folders(root, limit):
    if os.path.exists(root):
        shutil.rmtree(root)

    os.mkdir(root)

    os.chdir(root)
    make_subfolders(limit)
    os.chdir('..')

print(os.path.abspath('.'))
make_folders('TEST', 100)

