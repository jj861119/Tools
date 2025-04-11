from Crypto.Cipher import AES # pip install pycryptodome
from binascii import a2b_hex

key = 'password'.encode('utf-8')
mode = AES.MODE_CBC
iv = b'my_iv'

def decrypt(byte_string):
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(byte_string))
    plain_text_bytes = plain_text.rstrip(b'\0')[:-1]
    return plain_text_bytes

if __name__ == '__main__':
    import cv2
    from object_detection import predict, \
                                wrap_prediction, \
                                format_yolov5
    content = open('models/coco2014_3class_v5s_encrypted','rb').read()
    data = decrypt(content)
    net = cv2.dnn.readNetFromONNX(data)
    if cv2.cuda.getCudaEnabledDeviceCount() > 0:
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    input_img = cv2.imread("img000410.jpg")
    
    input_img = format_yolov5(input_img)
    outs = predict(input_img, net, 640, 640)
    class_ids, confidences, bbox_ltwh = wrap_prediction(input_img, \
                                                        outs[0], \
                                                        640, \
                                                        640, \
                                                        0.4, \
                                                        0.45, \
                                                        classes=None)



    print(class_ids, confidences, bbox_ltwh)