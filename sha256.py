# Cryptography I Assignment Week 3 Hash Function Implementation
import binascii
from Crypto.Hash import SHA256

# Function to hash iteratively
def hash_iteration(kbl):
    hl = list()
    for i in reversed(range(len(kbl))):
        if i == len(kbl)-1:
            sha = SHA256.new()
            sha.update(''.join(kbl[i]))
            hl.append(sha.digest())
        else:
            '''my_hexdata = hl[-1]
            scale = 16 ## equals to hexadecimal
            # num_of_bits = 8
            hb = bin(int(my_hexdata, scale))[2:] # .zfill(num_of_bits)'''
            h = ''.join(kbl[i]) + hl[-1]
            sha = SHA256.new()
            sha.update(h)
            hl.append(sha.digest())
    return hl

filepath = "C:\cw3pa\a.mp4"

# Read file into byte array
byte_list = list()
with open(r"C:\cw3pa\b.mp4", "rb") as f:
    byte = f.read(1)
    while byte != '':
        # b = ''.join(s.encode('hex') for s in byte)
        byte_list.append(byte)
        byte = f.read(1)


# Divide byte array into KB array:
kb_list = list()
for i in range(len(byte_list)):
    if i!=0 and i % 1024 == 0:
        kb_list.append(byte_list[i-1024:i])
    elif i == len(byte_list)-1:
        kb_list.append(byte_list[i-(i%1024):i+1])

hash_list = hash_iteration(kb_list)

# print hash_list[0]
print ''.join(s.encode('hex') for s in hash_list[-1])
        

'''hexadecimal = binascii.hexlify(byte)
    decimal = int(hexadecimal, 16)
    binary = bin(decimal)[2:].zfill(8)
    print("hex: %s, decimal: %s, binary: %s" % (hexadecimal, decimal, binary))'''



