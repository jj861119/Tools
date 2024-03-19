import os 
import shutil

files = [f for f in os.listdir()]
for file in files:
    tmp = file.split('_')
    if tmp[3]=='time.txt':
        continue
    # print(f'{tmp[0]}_{tmp[1]}_{tmp[2]}.txt')
    os.rename(file, f'{tmp[0]}_{tmp[1]}_{tmp[2]}.txt')