
import hashlib

def get_md5_data(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf8'))
    return md5.hexdigest()