import gmpy2

# Values for debugging (x0 = 1002, x1 = 783, val = 658308031, x = 1026831)
p_d = 1073676287
g_d = 1010343267
h_d = 857348958
B_d = 2**10
# Assignment values
p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
g = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
h = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333
B = 2**20


def hash_table(h, g, p, B):
    table = dict() # Table to store x1 and h/(g**x1) values
    for x1 in range(B-1):
        val = gmpy2.f_mod(gmpy2.mul(h, gmpy2.powmod(g, -x1, p)), p)
        table.update({val : x1})

    return table

def mit_in_the_middle(h, g, p, B):
    tab = hash_table(h, g, p, B)
    for x in range(B-1):
        val = gmpy2.powmod(g, gmpy2.mul(B, x), p)
        if val in tab:
            # print val
            x0 = x
            x1 = tab[val]
            # print x0, x1

    return gmpy2.mul(x0, B) + x1

print mit_in_the_middle(h, g, p, B)
        
