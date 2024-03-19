import cv2
import glob
import os
 
img_array = []
for filename in sorted(glob.glob('D:/Github/DDRNet.pytorch/test_results2/*.png'), 
                        key=os.path.getmtime):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
 
out = cv2.VideoWriter('CCD2_07_cut_result.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()