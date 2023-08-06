from ._base import floatish_T, scalar_or_sequence_or_floatish_T, ndarray_T, dtype_T
from ._base import _polynomial_base_with_t_ref, arr_constructor, arr_zeros_constructor

from .shared import horner

from collections.abc import Sequence
from typing import Union, Optional


class NewtonBase(_polynomial_base_with_t_ref):
    """
    NewtonBase

    represents polynomials in Newton base representation and uses Horner to evaluate and differentiate;
    polynomials in Newton base can be represented mathematically as:

        p(t) = coeff[:, 0] + coeff[:, 1]*(t - t_ref[0]) + coeff[:, 2]*(t - t_ref[0])*(t - t_ref[1]) + ...
    """

    @classmethod
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[ndarray_T[floatish_T]] = None) -> 'NewtonBase':
        """
        pseudo-constructor
        """
        return cls(coeff = arr_zeros_constructor(shape = (dim, degree + 1)), t_ref = t_ref)

    def __init__(self,
                 coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None,
                 t_ref: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None):
        """
        constructor of monomial class

        Parameters
        ----------
        coeff: Optional[ndarray_T[floatish_T]], default = None
            1-dim or 2-dim array of coefficients of (potentially vectorized) polynomial (daefault is None)
        t_ref: Optional[floatish_T], default = 0.0
            reference points
        """
        super().__init__(coeff = coeff)
        self.t_ref = t_ref

    @property
    def t_ref(self) -> Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]:
        """
        placeholder
        """
        return self._t_ref

    @t_ref.setter
    def t_ref(self, _t_ref: Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]):
        if _t_ref is None: self._t_ref = None
        else:
            if isinstance(_t_ref, Sequence): _t_ref = arr_constructor(_t_ref, copy = False)
            if len(_t_ref.shape) != 1: raise AssertionError("shape of t_ref has to be: len(t_ref.shape) == 1!")
            self._t_ref = _t_ref

    def __call__(self,
                 t_arg: floatish_T,
                 cap_order_4_diff: Optional[int] = None,
                 outs: Optional = None,
                 dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]:
        """
        placeholder
        """
        return horner(coeff = self.coeff,
                      t_ref = self.t_ref,
                      t_arg = t_arg,
                      is_newton_base = True,
                      cap_order_4_diff = cap_order_4_diff,
                      outs = outs,
                      dtype = dtype)
