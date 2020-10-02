import hashlib

def compute_hashcode(filename, method='md5'):
    if method == 'md5':
        hashcode = hashlib.md5()
    elif method == 'sha1':
        hashcode = hashlib.sha1()
    else:
        raise ValueError('Currently only the methods md5 and sha1 are supported!')

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hashcode.update(chunk)

    return hashcode.hexdigest()