from Crypto.Cipher import AES # pip install pycryptodome
from binascii import b2a_hex

key = 'password'.encode('utf-8')
mode = AES.MODE_CBC
iv = b'my_iv'


def add_to_16(byte_string):
    byte_string = byte_string + b'\1'
    if len(byte_string) % 16:
        add = 16 - (len(byte_string) % 16)
    else:
        add = 0

    byte_string = byte_string + (b'\0' * add)
    return byte_string

def Encrypt(byte_string):
    byte_string = add_to_16(byte_string)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(byte_string)
    return b2a_hex(cipher_text)

if __name__ == '__main__':
    with open('coco2014_3class_v5s.onnx','rb') as f1:
    # with open('output/giant/asus/ddrnet23_slim_0210_finetune2/ddrnet23_slim_0210_finetune2.pth','rb') as f1:
        encrypted=Encrypt(f1.read())
        with open('coco2014_3class_v5s_encrypted','wb') as f2:
            f2.write(encrypted)
 
    exit(0)
