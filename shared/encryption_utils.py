import itertools, hashlib

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def encrypt(data, session_id=''):
    m = hashlib.sha1()

    encrypted_data = []
    for chunk in chunks(data, 2):
        dec = chunk
        enc = hashlib.sha1(session_id.encode() + dec).digest()
        # print(len(encrypted_data), enc, dec)
        encrypted_data.append(enc)

    return b''.join(encrypted_data)


def decrypt(encrypted_file_content, decrypt_map):
    file_contents = []
    for encrypted_chunk in chunks(encrypted_file_content, 20):
        # print(len(file_contents), encrypted_chunk)
        file_contents.append(decrypt_map[encrypted_chunk])

    file_content = b''.join(file_contents)

    return file_content

def generate_decrypt_map(key, data_size):
    decrypt_map = {}

    chrset = [ x for x in range(0, 256) ]
    for size in range(1, data_size+1):
        perms = itertools.product(chrset, repeat=size)
        for perm in perms:
            dec = bytes(perm)
            # print(key, chr(perm))
            enc = hashlib.sha1(key.encode() + dec).digest()
            # if dec=='RI' or dec == b'RI':
            # print(dec, enc)
            decrypt_map[enc] = dec
    # print(self.decrypt_map)
    return decrypt_map
