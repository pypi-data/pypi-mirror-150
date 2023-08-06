from random import sample


from .player import Player
from .util import *


from Crypto.Hash import SHA1


class ThresholdElGamal:

    """
    Threshold scheme for ElGamal cryptosystem.

    :param k: Threshold.
    :param n: Total number of players.
    :param length: Length of prime number p.
    :type k: int
    :type n: int
    :type length: int
    """

    def __init__(self, k=3, n=5, length=2048):

        if not all(isinstance(arg, int) for arg in [k, n, length]):
            raise ValueError("Type mismatch")

        if not 0 < k <= n:
            raise ValueError("Incorrect scheme parameters")

        self.k = k
        self.n = n
        self.length = length
        self.params = None
        self.params = self.get_or_generate_params()
        self.p = self.params['p']
        self.q = self.params['q']
        self.g = self.params['g']
        self.h = self.params['h']

    def get_or_generate_params(self):
        """
        Generates parameters for threshold scheme (p, q, g, h) if not already generated,
        and if so, returns them together with parameters k and n.

        :return: Dictionary of parameters for the scheme.
        :rtype: dict
        """
        if self.params is None:
            self.params = get_new_params(self.length)
        else:
            self.params['k'] = self.k
            self.params['n'] = self.n
        return self.params

    def encrypt(self, pk, message, r=None):

        """
        Encrypts given message with given public key using the ElGamal cryptosystem.

        :param pk: Public key.
        :type pk: gmpy2.mpz
        :param message: Message
        :type message: int
        :param r: r
        :type r: gmpy2.mpz
        :return: c1, c2
        :rtype: tuple
        """

        if not (isinstance(pk, gmpy2.mpz) and isinstance(message, int)):
            raise ValueError("Type mismatch")

        if not 0 < message < self.p:
            raise ValueError("Message must be in (0,p)")

        if not 0 < pk < self.p:
            raise ValueError("Invalid public key")

        if r is None:
            r = gmpy2.mpz_random(gmpy2.random_state(), self.p)
        elif not 0 < r < self.p:
            raise ValueError("Invalid r value")

        c1 = gmpy2.powmod(self.g, r, self.p)
        message_bytes = bin(message)[2:]

        yr = gmpy2.powmod(pk, r, self.p)
        yr_encoded = bytes(str(yr), 'utf-8')

        hyr = bin(int(SHA1.new(yr_encoded).hexdigest(), 16))[2:]

        c2 = [str(int(b1, 2) ^ int(b2, 2)) for b1, b2 in zip(message_bytes, hyr)]
        c2 = "".join(c2)

        return c1, c2

    def decrypt(self, c2, decryption_shares):

        """
        Runs a distributed decryption algorithm using the ElGamal cryptosystem.

        :param c2: c2
        :type c2: str
        :param decryption_shares: Decryption shares.
        :type decryption_shares: list
        :return: Decrypted message.
        :rtype: int
        """

        if not (isinstance(c2, str) and isinstance(decryption_shares, dict)):
            raise ValueError("Type mismatch")

        if not (self.k <= len(decryption_shares.keys()) <= self.n and all(isinstance(arg, gmpy2.mpz) for arg in decryption_shares.values())):
            raise ValueError("Invalid decryption shares")

        product = gmpy2.mpz(1)
        if self.k > len(decryption_shares.keys()):
            raise ValueError("Not enough valid shares to decrypt.")
        selected_shares = sample(decryption_shares.keys(), self.k)

        for id_ in selected_shares:
            share = decryption_shares[id_]
            lagrange = calculate_lagrange_coeff(id_, selected_shares, self.q)
            d_lagrange = gmpy2.powmod(share, lagrange, self.p)
            product = gmpy2.mul(product, d_lagrange)
            product = gmpy2.mod(product, self.p)

        product_encoded = bytes(str(product), 'utf-8')
        hash_prod = bin(int(SHA1.new(product_encoded).hexdigest(), 16))[2:]
        message_bytes = [str(int(b1, 2) ^ int(b2, 2)) for b1, b2 in zip(hash_prod, c2)]
        message = "".join(message_bytes)
        message = int(message, 2)

        return message


def create_tc_scheme(k, n, length=2048):

    """
    Creates an ElGamal threshold scheme.

    :param length: Length of prime number p.
    :param k: Threshold.
    :param n: Total number of players.
    :type k: int
    :type n: int
    :type length: int
    :return: Public key y, list of players, scheme.
    :rtype: tuple
    """

    scheme = ThresholdElGamal(k, n, length)
    params = scheme.get_or_generate_params()
    players = [Player(i, params) for i in range(1, n + 1)]

    commits = {pl: pl.commit() for pl in players}

    for pl in players:
        pl.send_shares(players)

    for pl in players.copy():
        pl.check_shares(commits, players)

    players = players[0].honest_players

    commits_pk = {pl: pl.commit_pk() for pl in players}
    failed_shares = dict()
    for pl in players:
        pl.check_pk_commits(commits_pk, failed_shares)

    recalculated_commits = dict()
    for pl, points in failed_shares.items():
        z = reconstruct_polynomial(points, scheme.k - 1, scheme.q)
        recalculated_commits[pl] = scheme.g ** z % scheme.p

    for pl in recalculated_commits.keys():
        commits_pk[pl] = [recalculated_commits[pl]]

    for pl in players:
        pl.construct_pk(commits_pk)

    y = players[0].get_pk()

    return y, players, scheme


def run_tc_scheme(k, n, m, length=2048):

    """
    Runs an ElGamal threshold scheme.

    :param length: Length of prime number p.
    :type length: int
    :param k: Threshold.
    :type k: int
    :param n: Total number of players.
    :type n: int
    :param m: Message.
    :type m: int
    :return: The validity of the run scheme.
    :rtype: bool
    """

    y, players, scheme = create_tc_scheme(k, n, length)
    c1, c2 = scheme.encrypt(y, m)
    decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
    m_ = scheme.decrypt(c2, decryption_shares)
    return m_ == m
