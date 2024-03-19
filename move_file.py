import os 
import shutil

dest_dir = os.path.dirname(os.path.abspath(__file__))

dirs = [f for f in os.listdir() if os.path.isdir(f)]
for dir in dirs:
    files = [f for f in os.listdir(os.path.join(dest_dir,dir))]
    for file in files:
        # pass
        # print(os.path.join(dest_dir,dir,file))
        shutil.move(os.path.join(dest_dir,dir,file), dest_dir)