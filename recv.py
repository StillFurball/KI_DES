import socket

def str_to_bin(txt):
    return ''.join(format(ord(c), '08b') for c in txt)

def bin_to_str(b):
    return ''.join(chr(int(b[i:i+8], 2)) for i in range(0, len(b), 8))

def bin_to_hex(b):
    return ''.join(format(int(b[i:i+4], 2), 'x') for i in range(0, len(b), 4))

def hex_to_bin(h):
    return ''.join(format(int(c, 16), '04b') for c in h)

init_perm = [58,50,42,34,26,18,10,2, 60,52,44,36,28,20,12,4,
             62,54,46,38,30,22,14,6, 64,56,48,40,32,24,16,8,
             57,49,41,33,25,17,9,1,  59,51,43,35,27,19,11,3,
             61,53,45,37,29,21,13,5, 63,55,47,39,31,23,15,7]

final_perm = [40,8,48,16,56,24,64,32, 39,7,47,15,55,23,63,31,
              38,6,46,14,54,22,62,30, 37,5,45,13,53,21,61,29,
              36,4,44,12,52,20,60,28, 35,3,43,11,51,19,59,27,
              34,2,42,10,50,18,58,26, 33,1,41,9,49,17,57,25]

expansion_perm = [32,1,2,3,4,5, 4,5,6,7,8,9, 8,9,10,11,12,13, 12,13,14,15,16,17,
                  16,17,18,19,20,21, 20,21,22,23,24,25, 24,25,26,27,28,29, 28,29,30,31,32,1]

key_pc1 = [57,49,41,33,25,17,9, 1,58,50,42,34,26,18, 10,2,59,51,43,35,27, 19,11,3,60,52,44,36,
           63,55,47,39,31,23,15, 7,62,54,46,38,30,22, 14,6,61,53,45,37,29, 21,13,5,28,20,12,4]

key_pc2 = [14,17,11,24,1,5,3,28, 15,6,21,10,23,19,12,4, 26,8,16,7,27,20,13,2,
           41,52,31,37,47,55,30,40, 51,45,33,48,44,49,39,56, 34,53,46,42,50,36,29,32]

shift_table = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

permutate = [16,7,20,21,29,12,28,17, 1,15,23,26,5,18,31,10,
             2,8,24,14,32,27,3,9, 19,13,30,6,22,11,4,25]

sbox = [
 [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],[0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
  [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],[15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
 [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],[3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
  [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],[13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
 [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],[13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
  [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],[1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
 [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],[13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
  [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],[3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
 [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],[14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
  [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],[11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
 [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],[10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
  [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],[4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
 [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],[13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
  [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],[6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
 [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],[1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
  [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],[2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]],
]

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def shift_left(bits, n):
    return bits[n:] + bits[:n]

def generate_subkeys(key64):
    k = permute(key64, key_pc1)          # 56 bit
    l, r = k[:28], k[28:]
    subkeys = []
    for s in shift_table:
        l, r = shift_left(l, s), shift_left(r, s)
        subkeys.append(permute(l + r, key_pc2))  # 48 bit
    return subkeys

def feistel(r, subkey):
    x = xor(permute(r, expansion_perm), subkey)   # 48 bit
    out = ''
    for i in range(8):
        chunk = x[i*6:(i+1)*6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        out += format(sbox[i][row][col], '04b')
    return permute(out, permutate)                # 32 bit

def des_block(block64, subkeys):
    b = permute(block64, init_perm)
    l, r = b[:32], b[32:]
    for sk in subkeys:
        l, r = r, xor(l, feistel(r, sk))
    return permute(r + l, final_perm)             # swap terakhir + FP

def pad(data):                                    # PKCS#7 (byte)
    n = 8 - len(data) % 8
    return data + bytes([n]) * n

def unpad(data):
    return data[:-data[-1]]

def bytes_to_bin(bs):
    return ''.join(format(b, '08b') for b in bs)

def bin_to_bytes(b):
    return bytes(int(b[i:i+8], 2) for i in range(0, len(b), 8))

def make_key(key_text):
    kb = key_text.encode('utf-8')
    if len(kb) != 8:
        raise ValueError("Key harus tepat 8 karakter (64 bit)")
    return bytes_to_bin(kb)

def encrypt(plaintext, key_text):
    subkeys = generate_subkeys(make_key(key_text))
    data = bytes_to_bin(pad(plaintext.encode('utf-8')))
    ct = ''.join(des_block(data[i:i+64], subkeys) for i in range(0, len(data), 64))
    return bin_to_hex(ct)

def decrypt(cipher_hex, key_text):
    subkeys = generate_subkeys(make_key(key_text))[::-1]   
    data = hex_to_bin(cipher_hex)
    pt = ''.join(des_block(data[i:i+64], subkeys) for i in range(0, len(data), 64))
    return unpad(bin_to_bytes(pt)).decode('utf-8')


HOST, PORT = "0.0.0.0", 5000
KEY = "Sandi123"          

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Menunggu koneksi di {HOST}:{PORT} ...")
        conn, addr = s.accept()
        with conn:
            chunks = []
            while True:
                d = conn.recv(4096)
                if not d:
                    break
                chunks.append(d)
    cipher = b''.join(chunks).decode()
    print("Ciphertext diterima:", cipher)
    print("Plaintext hasil dekripsi:", decrypt(cipher, KEY))