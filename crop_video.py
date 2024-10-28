import cv2
import numpy as np
from os import path

source = 'E:/datasets/cupola360/roi_1_short.mp4'
cap = cv2.VideoCapture(source)
ret, frame = cap.read()
h, w, c = frame.shape
print(frame.shape)

left = 0
right = 1920
top = 420
bottom = 1500

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
source_path = source.rsplit("/", maxsplit=1)[0]
source_name = source.rsplit("/", maxsplit=1)[1].split('.')[0]
output_path = f'{source_path}/{source_name}_resized.mp4'
if path.isfile(output_path):
    raise Exception('output file name already exist')
out = cv2.VideoWriter(output_path, fourcc, 30.0, (right-left, bottom-top))
print(output_path)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.namedWindow('frame_cropped', cv2.WINDOW_NORMAL)
while ret:
    # frame_cropped = frame[top:bottom, left:right, :]
    frame_cropped = cv2.resize(frame, (1920,1080))
    out.write(np.ascontiguousarray(frame_cropped))
    cv2.imshow('frame', frame)
    cv2.imshow('frame_cropped', frame_cropped)
    cv2.waitKey(5)
    ret, frame = cap.read()
cap.release()
out.release()
