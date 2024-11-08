from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from datetime import datetime, timedelta, timezone
date = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)).date().isoformat()

data = date.encode("utf-8")

recipient_key = RSA.import_key(open("public.pem").read())
session_key = get_random_bytes(32)

# Encrypt the session key with the public RSA key

cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
print(ciphertext)
print(ciphertext.hex())
print(bytes.fromhex(ciphertext.hex()))


with open("encrypted_data.bin", "wb") as f:
    f.write(enc_session_key)
    f.write(cipher_aes.nonce)
    f.write(tag)
    f.write(ciphertext)


private_key = RSA.import_key(open("private.pem").read())

with open("encrypted_data.bin", "rb") as f:
    enc_session_key = f.read(private_key.size_in_bytes())
    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read()

# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
datetime_str = data.decode("utf-8")

datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d')
today = (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=24)).date()
print(today)
print(datetime_object.date())
print((datetime_object.date() - today).days)