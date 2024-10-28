import cv2
 
rtsp_ip = 'rtsp://192.168.1.100/streaming'
cam = cv2.VideoCapture(rtsp_ip,
                        apiPreference=cv2.CAP_FFMPEG,
                        params=[cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 1000])
ret, img = cam.read()
height, width, c = img.shape
size = (width, height)
out = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
count = 0
while True:
    ret, frame = cam.read()
    if not ret:
        cam.release()
        cam.open(rtsp_ip,
                apiPreference=cv2.CAP_FFMPEG,
                params=[cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 1000])
        print('Camera reconnected')
        continue

    cv2.imshow('frame', frame)
    key = cv2.waitKey(3)
    out.write(frame)
    count+=1
    if count>=9000:
        break
out.release()
 