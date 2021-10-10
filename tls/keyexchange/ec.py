import gmpy2


class EcField:
    """
    Elliptic Curve Field. It is used for ECDHE (Elliptic Curve Diffie Hellman Ephemeral)

    y^2 = x^3 + ax + b
    """

    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod

    def mod_inv(self, a):
        return gmpy2.invert(a, self.mod)

    def included(self, x, y):
        return (y ** 2 - x ** 3 - self.a * x - self.b) % self.mod == 0


class EcPoint:
    """
    Single point on the EcField or the y-limit which has mod value as y value
    """

    def __init__(self, x, y, f: EcField):
        if y != f.mod:
            assert f.included(x, y)

        self.f = f
        self.x = x
        self.y = y

    def __eq__(self, other):
        assert self.f.a == other.f.a and self.f.b == other.f.b and self.f.mod == other.f.mod
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if other.y == self.f.mod:
            return self
        if self.y == self.f.mod:
            return other

        if self == other:
            if self.y == 0:
                return EcPoint(0, self.f.mod, self.f)
            s = ((3 * (self.x ** 2) + self.f.a) * self.f.mod_inv(2 * self.y)) % self.f.mod
        else:
            if self.x == other.x:
                return EcPoint(self.x, self.f.mod, self.f)
            s = ((other.y - self.y) * self.f.mod_inv(other.x - self.x)) % self.f.mod

        next_x = (s ** 2 - self.x - other.x) % self.f.mod
        next_y = (s * (self.x - next_x) - self.y) % self.f.mod
        return EcPoint(
            next_x if next_x > 0 else next_x + self.f.mod,
            next_y if next_y > 0 else next_y + self.f.mod,
            self.f
        )

    def __mul__(self, other):
        ret = EcPoint(0, self.f.mod, self.f)
        cur = EcPoint(self.x, self.y, self.f)
        bits = []
        while other > 0:
            bits.append(other % 2 == 1)
            other >>= 1

        for bit in bits:
            if bit:
                ret = ret + cur
            cur = cur + cur

        return ret

    def __rmul__(self, other):
        return self * other


if __name__ == '__main__':
    field = EcField(gmpy2.mpz(2), gmpy2.mpz(2), gmpy2.mpz(17))
    point = EcPoint(gmpy2.mpz(5), gmpy2.mpz(1), field)
    for i in range(20):
        new_point = point * (i + 1)
        print((new_point.x, new_point.y))

    xA = point * 3
    xB = point * 7
    assert xA * 7 == xB * 3
