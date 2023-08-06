import random

from threshold_elgamal import run_tc_scheme, create_tc_scheme, Player, ThresholdElGamal
from threshold_elgamal.util import *
import unittest


class TCTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_simple(self):
        res = run_tc_scheme(3, 5, 10)
        self.assertTrue(res)

    def test_bigger(self):
        res = run_tc_scheme(5, 7, 10)
        self.assertTrue(res)

    def test_1_of_n_scheme(self):
        res = run_tc_scheme(1, 5, 10)
        self.assertTrue(res)

    def test_n_of_n_scheme(self):
        res = run_tc_scheme(5, 5, 10)
        self.assertTrue(res)

    def test_1_of_1_scheme(self):
        res = run_tc_scheme(1, 1, 10)
        self.assertTrue(res)

    def test_incorrect_scheme(self):
        self.assertRaises(ValueError, run_tc_scheme, 6, 5, 10)

    def test_incorrect_scheme_zero(self):
        self.assertRaises(ValueError, run_tc_scheme, 0, 6, 10)

    def test_incorrect_msg(self):
        self.assertRaises(ValueError, run_tc_scheme, 5, 6, "message")

    def test_msg_too_large(self):
        y, _, scheme = create_tc_scheme(3, 5)
        message = scheme.p + 50
        self.assertRaises(ValueError, scheme.encrypt, y, message)

    def test_3072_scheme(self):
        res = run_tc_scheme(3, 5, 10, 3072)
        self.assertTrue(res)

    def test_4096_scheme(self):
        res = run_tc_scheme(3, 5, 10, 4096)
        self.assertTrue(res)


class ManualTCTestCase(unittest.TestCase):

    def test_manual_scheme(self):
        y, players, scheme = create_tc_scheme(3, 5)
        c1, c2 = scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = scheme.decrypt(c2, decryption_shares)
        self.assertTrue(10 == dec_msg)

    def test_manual_1_of_n_scheme(self):
        y, players, scheme = create_tc_scheme(1, 5)
        c1, c2 = scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = scheme.decrypt(c2, decryption_shares)
        self.assertTrue(10 == dec_msg)

    def test_manual_1_of_1_scheme(self):
        y, players, scheme = create_tc_scheme(1, 1)
        c1, c2 = scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = scheme.decrypt(c2, decryption_shares)
        self.assertTrue(10 == dec_msg)

    def test_manual_n_of_n_scheme(self):
        y, players, scheme = create_tc_scheme(5, 5)
        c1, c2 = scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = scheme.decrypt(c2, decryption_shares)
        self.assertTrue(10 == dec_msg)

    def test_manual_incorrect_scheme(self):
        y, players, scheme = create_tc_scheme(3, 5)
        c1, c2 = scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        new_shares = random.sample(decryption_shares.keys(), 2)
        new_shares = {idx: decryption_shares[idx] for idx in new_shares}
        self.assertRaises(ValueError, scheme.decrypt, c2, new_shares)

    def test_manual_incorrect_scheme2(self):
        y, players, scheme = create_tc_scheme(3, 5)
        c1, c2 = scheme.encrypt(y, 10)
        self.assertRaises(ValueError, scheme.decrypt, c2, [])


class PlayerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.scheme = ThresholdElGamal()
        self.params = self.scheme.get_or_generate_params()
        self.missing_params = self.params.copy()
        del self.missing_params["k"]
        self.incorrect_params = self.missing_params.copy()
        self.incorrect_params["k"] = "string"

    def test_player_creation_string(self):
        self.assertRaises(ValueError, Player, "string", self.params)

    def test_player_creation_empty_list(self):
        self.assertRaises(ValueError, Player, 1, dict())

    def test_player_creation_missing_param(self):
        self.assertRaises(ValueError, Player, 1, self.missing_params)

    def test_player_creation_incorrect_param(self):
        self.assertRaises(ValueError, Player, 1, self.incorrect_params)


class DishonestPlayerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.scheme = ThresholdElGamal(3, 5)
        self.params = self.scheme.get_or_generate_params()

    def test_one_dishonest_player(self):
        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        commits = {pl: pl.commit() for pl in players}
        misfit = players[random.randint(0, self.scheme.n-1)]
        misfit.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        self.assertNotIn(misfit, players)

    def test_two_dishonest_players(self):
        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        commits = {pl: pl.commit() for pl in players}

        misfit1 = players[random.randint(0, self.scheme.n-1)]
        misfit1.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)
        misfit2 = players[(misfit1.id + 1) % self.scheme.n]
        misfit2.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        self.assertNotIn(misfit1, players)
        self.assertNotIn(misfit2, players)

    def test_t_dishonest_players(self):
        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        commits = {pl: pl.commit() for pl in players}

        misfits = random.sample(players, self.scheme.k - 1)
        for m in misfits:
            m.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        for m in misfits:
            self.assertNotIn(m, players)

    def test_dishonest_reconstruction(self):

        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        commits = {pl: pl.commit() for pl in players}

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        misfit = random.sample(players, 1)[0]
        old_polynomial = misfit.a
        misfit.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        commits_pk = {pl: pl.commit_pk() for pl in players}
        failed_shares = dict()
        for pl in players:
            pl.check_pk_commits(commits_pk, failed_shares)

        recalculated_commits = dict()
        for i, points in failed_shares.items():
            z = reconstruct_polynomial(points, self.scheme.k, self.scheme.q)
            self.assertEqual(z, old_polynomial[0])
            recalculated_commits[i] = gmpy2.powmod(self.scheme.g, z, self.scheme.p)

    def test_dishonest_pk_shares(self):

        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        commits = {pl: pl.commit() for pl in players}

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        misfit = random.sample(players, 1)[0]
        misfit.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        commits_pk = {pl: pl.commit_pk() for pl in players}
        failed_shares = dict()
        for pl in players:
            pl.check_pk_commits(commits_pk, failed_shares)

        recalculated_commits = dict()
        for pl, points in failed_shares.items():
            z = reconstruct_polynomial(points, self.scheme.k, self.scheme.q)
            recalculated_commits[pl] = gmpy2.powmod(self.scheme.g, z, self.scheme.p)

        for pl in recalculated_commits.keys():
            commits_pk[pl] = [recalculated_commits[pl]]

        for pl in players:
            pl.construct_pk(commits_pk)

        y = players[0].get_pk()

        c1, c2 = self.scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = self.scheme.decrypt(c2, decryption_shares)
        self.assertEqual(dec_msg, 10)

    def test_t_dishonest_pk_shares(self):

        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        commits = {pl: pl.commit() for pl in players}

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        misfits = random.sample(players, self.scheme.k - 1)
        for misfit in misfits:
            misfit.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        commits_pk = {pl: pl.commit_pk() for pl in players}
        failed_shares = dict()
        for pl in players:
            pl.check_pk_commits(commits_pk, failed_shares)

        recalculated_commits = dict()
        for pl, points in failed_shares.items():
            z = reconstruct_polynomial(points, self.scheme.k - 1, self.scheme.q)
            recalculated_commits[pl] = gmpy2.powmod(self.scheme.g, z, self.scheme.p)

        for pl in recalculated_commits.keys():
            commits_pk[pl] = [recalculated_commits[pl]]

        for pl in players:
            pl.construct_pk(commits_pk)

        y = players[0].get_pk()

        c1, c2 = self.scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = self.scheme.decrypt(c2, decryption_shares)
        self.assertEqual(dec_msg, 10)

    def test_dishonest_player_and_pk_shares(self):
        players = [Player(i, self.params) for i in range(1, self.scheme.n + 1)]
        # commits = [pl.commit() for pl in players]
        commits = {pl: pl.commit() for pl in players}

        misfits = random.sample(players, self.scheme.k - 1)
        for m in misfits:
            m.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        for pl in players:
            pl.send_shares(players)

        for pl in players.copy():
            pl.check_shares(commits, players)

        for m in misfits:
            self.assertNotIn(m, players)

        misfits = random.sample(players, 1)
        for misfit in misfits:
            misfit.a = construct_random_polynomial(self.scheme.k - 1, self.scheme.q)

        commits_pk = {pl: pl.commit_pk() for pl in players}
        failed_shares = dict()
        for pl in players:
            pl.check_pk_commits(commits_pk, failed_shares)

        recalculated_commits = dict()
        for i, points in failed_shares.items():
            z = reconstruct_polynomial(points, self.scheme.k - 1, self.scheme.q)
            recalculated_commits[i] = gmpy2.powmod(self.scheme.g, z, self.scheme.p)

        for i in recalculated_commits.keys():
            commits_pk[i] = [recalculated_commits[i]]

        for pl in players:
            pl.construct_pk(commits_pk)

        y = players[0].get_pk()

        c1, c2 = self.scheme.encrypt(y, 10)
        decryption_shares = {pl.id: pl.get_decryption_share(c1) for pl in players}
        dec_msg = self.scheme.decrypt(c2, decryption_shares)
        self.assertEqual(dec_msg, 10)


class UtilTestCase(unittest.TestCase):

    def test_reconstruct_polynomial(self):
        coeffs = construct_random_polynomial(3, 499)
        points = [(i, polynomial(coeffs, i, 499)) for i in range(1, 8)]
        z = reconstruct_polynomial(points, 3, 499)
        self.assertEqual(z, coeffs[0])

    def test_reconstruct_polynomial_big(self):
        coeffs = construct_random_polynomial(10, 499)
        points = [(i, polynomial(coeffs, i, 499)) for i in range(1, 20)]
        z = reconstruct_polynomial(points, 10, 499)
        self.assertEqual(z, coeffs[0])


def suite():
    suite_ = unittest.TestSuite()
    suite_.addTests([TCTestCase(), ManualTCTestCase(), PlayerTestCase(), UtilTestCase(), DishonestPlayerTestCase()])
    return suite_


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
