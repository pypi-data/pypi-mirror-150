from polynom import MonomialBase
import numpy as np
from typing import Optional, Union


class myFloat(object):

    def __init__(self, val : float):
        self.val : float = val

    def __str__(self) -> str: return f'<float: {self.val}>'

    def __repr__(self) -> str: return f'myFloat(val={self.val})'

    def __lin__(self,
                other : Union['myFloat', float],
                alpha : float = 1.0,
                beta : Optional[float] = None) -> 'myFloat':
        other : myFloat = self._check_other(other)
        if other is None: return myFloat(val=alpha*self.val)
        return myFloat(val=alpha*self.val + beta*other.val)

    @staticmethod
    def _check_other(other : Optional[Union['myFloat', float]] = None):
        if isinstance(other, float): return myFloat(val=other)
        elif not isinstance(other, myFloat): raise AssertionError('other has to be float or myFloat')
        return other

    def __pos__(self) -> 'myFloat': return self

    def __add__(self, other : Union['myFloat', float]) -> 'myFloat': return self.__lin__(other, 1.0, 1.0)

    def __radd__(self, other : float) -> 'myFloat': return self.__lin__(other, 1.0, 1.0)

    def __neg__(self) -> 'myFloat': return myFloat(val=-1.0*self.val)

    def __sub__(self, other : Union['myFloat', float]) -> 'myFloat': return self.__lin__(other, 1.0, -1.0)

    def __rsub__(self, other : float) -> 'myFloat': return self.__lin__(other, -1.0, 1.0)

    def __mul__(self, other : Union['myFloat', float]) -> 'myFloat':
        other = self._check_other(other)
        return myFloat(val=self.val*other.val)

    def __rmul__(self, other : float) -> 'myFloat': return self*other


mon_inst = MonomialBase(coeff = (myFloat(1.0), myFloat(-2.0)), t_ref = myFloat(0.1))
mon_inst_2 = MonomialBase(coeff = (1.0, -2.0), t_ref = 0.1)


out = mon_inst(myFloat(np.pi)), mon_inst(np.pi), mon_inst_2(np.pi)


assert abs(out[0][0, 0].val - out[1][0, 0].val) < 1.0e-14
assert abs(out[0][0, 0].val - out[2][0, 0]) < 1.0e-14
