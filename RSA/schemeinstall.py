import argparse
import rsa  # for keys
from util import auto_int, modinv
from sympy import randprime
from random import randint
from math import sqrt
from decimal import Decimal


def _print_params(filename, e, n, d, p, q, nn, dd):
    try:
        mystr = F"e = \"{hex(e)[2:]}\"\n" \
                F"n = \"{hex(n)[2:]}\"\n" \
                F"d = \"{hex(d)[2:]}\"\n" \
                F"p = \"{hex(p)[2:]}\"\n" \
                F"q = \"{hex(q)[2:]}\"\n" \
                F"sign_n = \"{hex(nn)[2:]}\"\n" \
                F"sign_d = \"{hex(dd)[2:]} \""
        with open(filename, "w") as file:
            file.write("This file should always be in place\n")
            file.write(mystr)
    except:
        print(F"e = \"{hex(e)[2:]}\"")
        print(F"n = \"{hex(n)[2:]}\"")
        print(F"d = \"{hex(d)[2:]}\"")
        print(F"p = \"{hex(p)[2:]}\"")
        print(F"q = \"{hex(q)[2:]}\"")

def _getNPQ(bits):
    p = randprime(2 ** ((bits // 2) - 1), 2 ** (bits // 2))
    q = randprime(2 ** ((bits // 2) - 1), 2 ** (bits // 2))
    p, q = max(p, q), min(p, q)
    n = p * q
    return n, p, q


def get_args():
    parser = argparse.ArgumentParser(description='RSA encoder and digital signature generator')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=1024,
                        help="Number of bits, default = 1024")

    parser.add_argument("-f",
                        help="file to save")

    parser.add_argument("--self",
                        action="store_true",
                        help="Use key-generation algorithm insted of rsa lib. Can use params")

    parser.add_argument("--wiener",
                        action="store_true",
                        help="Generate wiener-attack unimmune params")

    return parser.parse_args()


def gen_rsa(filename, bits):
    exp = 0x10001

    pubkey, privkey = rsa.newkeys(bits, exponent=exp)
    signpubkey, signprivkey = rsa.newkeys(1024, exponent=exp)

    _print_params(filename,
                  exp,
                  pubkey.n,
                  privkey.d,
                  privkey.p,
                  privkey.q,
                  signpubkey.n,
                  signprivkey.d)

def gen_rsa_wiener_vuln(filename, bits):
    n, p, q = _getNPQ(bits)
    n = Decimal(n)
    d = randint(0x10001, int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
    while True:
        try:
            e = modinv(d, (p - 1) * (q - 1))
        except:
            d = randint(0x10001, int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
            continue
        break
    n = int(n)
    _print_params(filename,
                  e, n, d, p, q, n, d
                  )


def gen_rsa_self(filename, bits):
    n, p, q = _getNPQ(bits)
    n = Decimal(n)
    d = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
    while True:
        try:
            e = modinv(d, (p - 1) * (q - 1))
        except:
            d = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                        int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
            continue
        break
    n = int(n)

    _print_params(filename,
                  e, n, d, p, q, n, d
                  )


if __name__ == '__main__':
    args = get_args()
    if args.wiener:
        gen_rsa_wiener_vuln(args.f, args.BITS)
    else:
        gen_rsa(args.f, args.BITS)
