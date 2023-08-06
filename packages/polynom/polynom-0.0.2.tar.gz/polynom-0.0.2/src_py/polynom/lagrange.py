from ._base import floatish_T, scalar_or_sequence_or_floatish_T, ndarray_T, dtype_T
from ._base import _polynomial_base_with_t_ref, arr_constructor, arr_empty_contructor, arr_zeros_constructor

from .shared import lagrange_poly_eval

from collections.abc import Sequence
from typing import Union, Optional


class LagrangeBase(_polynomial_base_with_t_ref):
    """
    placeholder
    """

    @classmethod
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[ndarray_T[floatish_T]] = None) -> 'LagrangeBase':
        """
        pseudo-constructor
        """
        return cls(coeff = arr_zeros_constructor(shape = (dim, degree + 1)), t_ref = t_ref)

    def __init__(self,
                 coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None,
                 t_ref: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None):
        """
        placeholder
        """
        super().__init__(coeff = coeff)
        self.t_ref = t_ref

        self.outs_lagrange_basis = None

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
                 outs: Optional = None,  # to recycle
                 outs_lagrange_basis: Optional = None,  # to recycle
                 dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]:
        lag_out = lagrange_poly_eval(coeff = self.coeff,
                                     t_ref = self.t_ref,
                                     t_arg = t_arg,
                                     cap_order_4_diff = cap_order_4_diff,
                                     outs = outs,  # to recycle
                                     outs_lagrange_basis = outs_lagrange_basis,  # to recycle
                                     dtype = dtype)
        self.outs_lagrange_basis = lag_out[1]
        return lag_out[0]  # out[0], ggf. out[1] save internally
