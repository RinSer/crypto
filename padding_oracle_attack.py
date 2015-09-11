import urllib2
import sys


cypher_text = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

proxy = urllib2.ProxyHandler({'http': 'http://username:password@192.168.0.152:8080'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding

if __name__ == "__main__":
    po = PaddingOracle()
    # po.query(sys.argv[1])       # Issue HTTP query with the given argument


def divideCypher(cypher_string):
    cypher_blocks = list()
    for i in range(len(cypher_string)+1):
        if i>0 and i%32 == 0:
            cypher_blocks.append(cypher_string[i-32:i])
    return cypher_blocks

def divideBlock(cyphers):
    block_list = list()
    for i in reversed(range(1, len(cyphers[-2]), 2)):
        block_list.append(cyphers[-2][i-1:i+1])
    return block_list

def decipherBlock(block_list, cypher_list):
    plain_int = list()
    for i in range(len(block_list)):
        if i == 0:
            for g in range(256):
                mutated = str(hex(int(block_list[i], 16) ^ g ^ i+1)[2:])
                if len(mutated) == 1:
                    mutated = '0' + mutated
                mutated_block = ''.join(reversed(block_list[i+1:])) + mutated
                cypher_list[-2] = mutated_block
                mutated_cypher = ''.join(cypher_list)
                if po.query(mutated_cypher) == True:
                    plain_int.append(g)
                    print g, chr(g)
                    break
        else:
            residue = list()
            for n in range(i):
                mutated_residue = str(hex(int(block_list[n], 16) ^ plain_int[n] ^ i+1)[2:])
                if len(mutated_residue) == 1:
                    mutated_residue = '0' + mutated_residue
                residue.append(mutated_residue)
            for g in range(256):
                mutated = str(hex(int(block_list[i], 16) ^ g ^ i+1)[2:])
                if len(mutated) == 1:
                    mutated = '0' + mutated
                mutated_block = ''.join(reversed(block_list[i+1:])) + mutated + ''.join(reversed(residue))
                cypher_list[-2] = mutated_block
                mutated_cypher = ''.join(cypher_list)
                if po.query(mutated_cypher) == True:
                    plain_int.append(g)
                    print g, chr(g)
                    break
                elif po.query(mutated_cypher) == None:
                    plain_int.append(i+1)
                    print i+1, chr(i+1)
                    break

    plain_block = ''
    for num in reversed(plain_int):
        plain_block = plain_block + chr(num)
        
    return plain_block

cypher2 = divideCypher(cypher_text)
cypher1 = divideCypher(cypher_text)[:3]
cypher0 = divideCypher(cypher_text)[:2]

plain_text_block_2 = decipherBlock(divideBlock(cypher2), cypher2)
plain_text_block_1 = decipherBlock(divideBlock(cypher1), cypher1)
plain_text_block_0 = decipherBlock(divideBlock(cypher0), cypher0)

plain_text = plain_text_block_0 + plain_text_block_1 + plain_text_block_2

print plain_text
