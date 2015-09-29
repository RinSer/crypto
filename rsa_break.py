# Bad RSA Break

import gmpy2
from extended_euclidean_algorithm import eea

gmpy2.get_context().precision = 1100 # Adjust calculations' precision
	

class Factorizer:
	def __init__(self, N):
		self.N = gmpy2.mpz(N)
		A = gmpy2.ceil(gmpy2.sqrt(self.N))
		x = gmpy2.sqrt(gmpy2.sub(pow(A, 2), self.N))
		self.p = gmpy2.mpz(gmpy2.sub(A, x))
		self.q = gmpy2.mpz(gmpy2.add(A, x))

	def get_p(self):
		return self.p

	def get_q(self):
		return self.q

	def check(self):
		if self.N == gmpy2.mul(self.p, self.q) and gmpy2.is_prime(self.p) and gmpy2.is_prime(self.q):
			return True


class FactorSearch:
	def __init__(self, N):
		self.N = gmpy2.mpz(N)
		A = gmpy2.ceil(gmpy2.sqrt(self.N))
		p = 0
		q = 0
		while self.N != gmpy2.mul(p, q):
			x = gmpy2.sqrt(gmpy2.sub(pow(A, 2), self.N))
			p = gmpy2.mpz(gmpy2.sub(A, x))
			q = gmpy2.mpz(gmpy2.add(A, x))
			A += 1
		self.p = p
		self.q = q

	def get_p(self):
		return self.p

	def check(self):
		if self.N == gmpy2.mul(self.p, self.q) and gmpy2.is_prime(self.p) and gmpy2.is_prime(self.q):
			return True


class FactorMult:
	def __init__(self, N):
		self.N = gmpy2.mpz(N)
		n24 = gmpy2.mul(self.N, 24)
		A = gmpy2.ceil(gmpy2.sqrt(n24))
		x = gmpy2.sqrt(gmpy2.sub(pow(A, 2), n24))
		p = gmpy2.mpz(gmpy2.sub(A, x))
		q = gmpy2.mpz(gmpy2.add(A, x))
		self.p = gmpy2.div(p, 6)
		self.q = gmpy2.div(q, 4)

	def get_p(self):
		return self.p

	def check(self):
		if self.N == gmpy2.mul(self.p, self.q) and gmpy2.is_prime(self.p) and gmpy2.is_prime(self.q):
			return True


class decipherRSA:
	def __init__(self, c, N, e, p, q):
		phi = gmpy2.mul(gmpy2.sub(p, 1), gmpy2.sub(q, 1))
		d = eea(e, phi)[1]
		if d < 0:
			d = gmpy2.f_mod(d, phi)
		plaintext = hex(gmpy2.powmod(c, d, N))
		plaintext = plaintext[2:]
		plaintext = plaintext.zfill(len(plaintext) + gmpy2.f_mod(len(plaintext), 2))
		plaintext = ' '.join(plaintext[i: i+2] for i in range(0, len(plaintext), 2))
		pad = plaintext.split(' ').index('00')
		hex_text = ''.join(plaintext.split(' ')[pad+1:])
		self.text = hex_text.decode('hex')
	
	def plaintext(self):
		return self.text



# Question 1
N1 = 179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581

challenge_1 = Factorizer(N1)
p = challenge_1.get_p()
q = challenge_1.get_q()
#print challenge_1.check()
print "Challenge #1 Answer:"
print p
print ''


# Question 2
N2 = 648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877

challenge_2 = FactorSearch(N2)
print "Challenge #2 Answer:"
print challenge_2.get_p()
#print challenge_2.check()
print ''


# Question 3
N3 = 720062263747350425279564435525583738338084451473999841826653057981916355690188337790423408664187663938485175264994017897083524079135686877441155132015188279331812309091996246361896836573643119174094961348524639707885238799396839230364676670221627018353299443241192173812729276147530748597302192751375739387929

challenge_3 = FactorMult(N3)
print "Challenge #3 Answer:"
print challenge_3.get_p()
#print challenge_3.check()
print ''


# Question 4
e = 65537

ciphertext = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

challenge_4 = decipherRSA(ciphertext, N1, e, p, q)
print "Challenge #4 Answer:"
print challenge_4.plaintext()