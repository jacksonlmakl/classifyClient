import secrets
import hashlib

def generate_token(email):
    md5_hash = hashlib.md5()
    md5_hash.update(email.encode('utf-8'))
    hash_md5 = md5_hash.hexdigest()
    # Generate a random 32-byte token in hexadecimal format
    s = secrets.token_hex(32)  # 32 bytes = 64 characters
    token=hash_md5+str(s)
    return token