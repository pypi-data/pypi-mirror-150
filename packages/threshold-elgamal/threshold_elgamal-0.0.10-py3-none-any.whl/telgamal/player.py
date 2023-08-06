from __future__ import annotations

import gmpy2

from .util import construct_random_polynomial, polynomial


class Player:

    """
    Player in a threshold ElGamal cryptosystem.

    :param i: Player identifier.
    :type i: int
    :param params: Parameters of the threshold scheme: primes p and q, generators g and h, total number of players n and threshold k.
    :type params: dict
    """

    def __init__(self, i, params):

        if not (isinstance(i, int) and isinstance(params, dict)):
            raise ValueError("Type mismatch")

        if {'g', 'h', 'q', 'p', 'n', 'k'} != set(params.keys()):
            raise ValueError("Parameters missing")

        if not all(isinstance(val, (gmpy2.mpz, int)) for val in params.values()):
            raise ValueError("Params type mismatch")

        self.id = i

        self.g, self.h = params['g'], params['h'],
        self.q, self.p = params['q'], params['p'],
        self.n, self.k = params['n'], params['k']
        self.t = self.k - 1

        self.a = construct_random_polynomial(self.t, self.q)
        self.b = construct_random_polynomial(self.t, self.q)
        self.f = lambda x: polynomial(self.a, x, self.q)
        self.f2 = lambda x: polynomial(self.b, x, self.q)

        self.pk = None
        self.received_shares = dict()
        self.received_shares2 = dict()
        self.decryption_share = None

        self.honest_players = None
        self.disqualified = False
        self.complaints_received = 0

    def __repr__(self):
        return f'Player({self.id})'

    def __str__(self):
        return f'Player {self.id}'

    def send_shares(self, players):
        """
        Sends a pair of shares to each of the players.

        :param players: List of players (including self).
        :type players: list
        """
        shares = [self.f(j) for j in range(1, self.n + 1)]
        shares2 = [self.f2(j) for j in range(1, self.n + 1)]
        for j, share, share2 in zip(players, shares, shares2):
            j.receive_share(self, share, share2)

    def commit(self):
        """
        Creates commitments for coefficient of the generated random polynomials.

        :return: Commitments.
        :rtype list:
        """
        commits = []
        for k in range(0, self.t+1):
            g_a = gmpy2.powmod(self.g, self.a[k], self.p)
            h_b = gmpy2.powmod(self.h, self.b[k], self.p)
            commit = gmpy2.mul(g_a, h_b)
            commit = gmpy2.mod(commit, self.p)
            commits.append(commit)
        return commits

    def commit_pk(self):
        """
        Generates commitments for the construction of the public key.

        :return: Commitments.
        :rtype: list
        """
        commits = []
        for k in range(0, self.t+1):
            g_a = gmpy2.powmod(self.g, self.a[k], self.p)
            commits.append(g_a)
        return commits

    def check_shares(self, commits, players):
        """
        Checks commitments for the shares and complains if the check fails.

        :param commits: Commitments.
        :type commits: dict
        :param players: List of players.
        :type players: list
        """
        if self.honest_players is None:
            self.honest_players = players
        for player in players:
            g_share = gmpy2.powmod(self.g, self.received_shares[player], self.p)
            h_share = gmpy2.powmod(self.h, self.received_shares2[player], self.p)
            check1 = gmpy2.mul(g_share, h_share)
            check1 = gmpy2.mod(check1, self.p)
            check2 = gmpy2.mpz(1)
            for k in range(0, self.t+1):
                exponent = self.id ** k
                factor = gmpy2.powmod(commits[player][k], exponent, self.p)
                check2 = gmpy2.mul(check2, factor)
                check2 = gmpy2.mod(check2, self.p)
            if check1 != check2:
                self.complain(player)

    def check_pk_commits(self, commits, failed_shares):
        """
        Checks commits for the construction of the public key. If any of the
        commits fail, the received share of that player is returned and used later
        when constructing the public key without the player's involvement.

        :param commits: Commitments.
        :type commits: dict
        :param failed_shares: Dictionary of received shares of players for whom the check failed. Used later while constructing the public key.
        :type failed_shares: dict
        """
        players = self.honest_players.copy()
        for i, player in enumerate(players):
            check1 = gmpy2.powmod(self.g, self.received_shares[player], self.p)
            product = gmpy2.mpz(1)
            for k in range(0, self.t+1):
                exponent = self.id ** k
                factor = gmpy2.powmod(commits[player][k], exponent, self.p)
                product = gmpy2.mul(product, factor)
                product = gmpy2.mod(product, self.p)
            check2 = gmpy2.mod(product, self.p)
            if check1 != check2:
                if player not in failed_shares:
                    failed_shares[player] = [(self.id, self.received_shares[player])]
                else:
                    temp = failed_shares[player]
                    temp.append((self.id, self.received_shares[player]))
                    failed_shares[player] = temp

    def get_pk(self):
        """
        Fetches the public key.

        :return: Public key.
        :rtype: gmpy2.mpz
        """
        if self.pk is None:
            raise ValueError("Public key not generated yet")
        else:
            return self.pk

    def construct_pk(self, commits):
        """
        Constructs public key from public key commitments.

        :param commits: Commitments.
        :type commits: dict
        """
        if self.pk is None:
            product = gmpy2.mpz(1)
            for i, pl in enumerate(self.honest_players):
                product = gmpy2.mul(commits[pl][0], product)
                product = gmpy2.mod(product, self.p)
            self.pk = product

    def construct_decryption_share(self, c1):
        """
        Constructs decryption share.

        :param c1: c1
        :type c1: gmpy2.mpz
        """
        if self.decryption_share is None:
            sum_ = gmpy2.mpz()
            for player, share in self.received_shares.items():
                if player not in self.honest_players:
                    continue
                sum_ = gmpy2.add(sum_, share)
                sum_ = gmpy2.mod(sum_, self.q)
            d_share = gmpy2.powmod(c1, sum_, self.p)
            self.decryption_share = d_share

    def get_decryption_share(self, c1):
        """
        Fetches the decryption share.

        :param c1: c1
        :type c1: gmpy2.mpz
        :return: Decryption share.
        :rtype: gmpy2.mpz
        """
        if self.decryption_share is None:
            self.construct_decryption_share(c1)
            return self.decryption_share
        else:
            return self.decryption_share

    def receive_share(self, player, share, share2):
        self.received_shares[player] = share
        self.received_shares2[player] = share2

    def complain(self, player):
        """
        Processes complains to player. If the player received more than t
        complaints, they are disqualified.

        :param player: Player.
        :type player: Player
        """
        player.complaints_received += 1
        if player.complaints_received > self.t:
            player.disqualified = True
            self.honest_players.remove(player)
