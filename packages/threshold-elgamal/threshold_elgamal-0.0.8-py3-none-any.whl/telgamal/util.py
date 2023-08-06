import secrets
import json

import gmpy2


def get_new_params(length=2048):
    """
    Generates new parameters for a threshold scheme. Fetches p, q, and g from a
    predefined list of groups. Then generates h by calculating g^(random number) mod p.

    :param length: Length of prime number p.
    :type length: int
    :return: (p, q, g, h) parameters for the scheme.
    :rtype: tuple
    """
    if length not in (2048, 3072, 4096):
        length = 2048
    with open('../params/groups.json') as json_file:
        data = json.load(json_file)['groups']
        group_params = data["ffdhe" + str(length)]
        rand_state = gmpy2.random_state()
        rand_tmp = gmpy2.mpz_random(rand_state, group_params['q'])
        p = gmpy2.mpz(group_params['p'])
        g = gmpy2.mpz(group_params['g'])
        q = gmpy2.mpz(group_params['q'])
        h = gmpy2.powmod(g, rand_tmp, p)
        group_params = {
            'p': p,
            'g': g,
            'q': q,
            'h': h
        }
        return group_params


def calculate_lagrange_coeff(i, idxs, q):
    """
    Calculates Lagrange coefficients.

    :param i: Index of the player.
    :type i: int
    :param idxs: Indexes of all players taking part in calculating the coefficient.
    :type idxs: list
    :param q: Modulo.
    :type q: int
    :return: Lagrange coefficient.
    :rtype: int
    """
    coeff = 1
    for j in idxs:
        if j == i:
            continue
        tmp = (j * gmpy2.invert(j - i, q)) % q
        coeff *= tmp
    coeff %= q
    return int(coeff)


def construct_random_polynomial(t, q):
    """
    Returns a list of random coefficients for a polynomial of degree `degree` modulo q.

    :param t: Degree of the polynomial.
    :type t: int
    :param q: Modulo.
    :type q: int
    :return: Coefficients of the random polynomial.
    :rtype: list
    """
    coefficients = []
    for _ in range(t + 1):
        coefficient = secrets.randbelow(q)
        coefficients.append(coefficient)
    return coefficients


def polynomial(coeffs, x, q):
    """
    Returns a y coordinate for a polynomial with given coefficients over field q.

    :param coeffs: Coefficients of the polynomial.
    :type coeffs: list
    :param x: x coordinate of the polynomial.
    :type x: gmpy2.mpz
    :param q: Modulo.
    :type q:
    :return: y coordinate.
    :rtype: gmpy2.mpz
    """
    point = gmpy2.mpz(0)
    for power, value in enumerate(coeffs):
        point = gmpy2.add(point, gmpy2.mul(gmpy2.powmod(x, power, q), value))
    return gmpy2.mod(point, q)


def reconstruct_polynomial(points, t, q):
    """
    Reconstructs coefficients of a polynomial given points, degree k and modulo q.

    :param points: Points on the polynomial.
    :type points: list
    :param q: Modulo.
    :type q: gmpy2.mpz
    :param t: Degree of the polynomial.
    :type t: int
    :return: Constant coefficient of the polynomial.
    :rtype: gmpy2.mpz
    """

    if len(points) < t + 1:
        raise ValueError("Not enough points to reconstruct.")

    x = [p[0] for p in points]
    y = [p[1] for p in points]

    x = x[:t + 1]
    y = y[:t + 1]

    z = gmpy2.mpz()
    for j in range(0, t + 1):
        prod = gmpy2.mpz(1)
        for m in range(0, t + 1):
            if m == j:
                continue
            else:
                inv_ = gmpy2.invert(x[m] - x[j], q)
                mul_ = gmpy2.mul(x[m], inv_)
                mod_ = gmpy2.mod(mul_, q)
                prod = gmpy2.mul(prod, mod_)
        z = gmpy2.add(gmpy2.mul(y[j], prod), z)
        z = gmpy2.mod(z, q)

    return z
