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
        encrypted_data.append(enc)
        # print(len(encrypted_data[-1]))

    return b''.join(encrypted_data)


def decrypt(encrypted_file_content, decrypt_map):
    file_contents = []
    for encrypted_chunk in chunks(encrypted_file_content, 20):
        # print(len(file_contents), file_contents)
        file_contents.append(decrypt_map[encrypted_chunk])

    file_content = b''.join(file_contents)

    return file_content

def generate_decrypt_map(key, data_size):
    decrypt_map = {}

    chrset = [ x for x in range(0, 256) ]
    perms = itertools.product(chrset, repeat=data_size)
    for perm in perms:
        dec = bytes(perm)
        # print(key, chr(perm))
        enc = hashlib.sha1(key.encode() + dec).digest()
        # if dec=='RI' or dec == b'RI':
        # print(dec, enc)
        decrypt_map[enc] = dec
    # print(self.decrypt_map)
    return decrypt_map
