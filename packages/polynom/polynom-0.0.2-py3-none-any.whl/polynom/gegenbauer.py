from ._base import floatish_T, scalar_or_sequence_or_floatish_T, ndarray_T, dtype_T
from ._base import _polynomial_base, arr_zeros_constructor, arr_ones_constructor

from .shared import gegenbauer_gen, _get_t_arg_and_shape

from collections.abc import Sequence
from typing import Union, Optional, Callable


class GegenbauerBase(_polynomial_base):
    """
    placeholder
    """
    _alpha: floatish_T = None
    _gegenbauer_eval: Callable = None

    @classmethod
    def zeros(cls, alpha: floatish_T, degree: int, dim: int = 1,
              domain : tuple[float, float] = (-1.0, 1.0)) -> 'GegenbauerBase':
        """
        pseudo-constructor
        """
        return cls(alpha = alpha, coeff = arr_zeros_constructor(shape = (dim, degree + 1)), domain = domain)

    def __init__(self,
                 alpha: floatish_T,
                 coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None,
                 domain : tuple[float, float] = (-1.0, 1.0)):
        """
        placeholder
        """
        super().__init__(coeff = coeff)

        self.alpha: floatish_T = alpha

        self.outs_P_prev = None
        self.outs_P_curr = None
        self.outs_P_succ = None

        self.domain : tuple[float, float] = domain

    @property
    def alpha(self): return self._alpha

    @alpha.setter
    def alpha(self, new_alpha: floatish_T):
        self._alpha = new_alpha
        self._gegenbauer_eval, _ = gegenbauer_gen(self.alpha)

    def transform_t_arg(self, t_arg):
        t_arg, shape_arg = _get_t_arg_and_shape(t_arg = t_arg)

        m = 2.0/(self.domain[1] - self.domain[0])
        d_t_arg = arr_ones_constructor(shape = shape_arg)
        return 1.0 - m*(self.domain[1] - t_arg), m*d_t_arg  # 1 - 2(b - x)/(b - a)

    def __call__(self,
                 t_arg: floatish_T,
                 cap_order_4_diff: Optional[int] = None,
                 outs: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                 outs_P_prev: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                 outs_P_curr: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                 outs_P_succ: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                 dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]:
        """
        placeholder
        """
        t_arg, d_t_arg = self.transform_t_arg(t_arg = t_arg)
        geg_out = self._gegenbauer_eval(self.coeff,
                                        t_arg = t_arg,
                                        d_t_arg = d_t_arg,
                                        cap_order_4_diff = cap_order_4_diff,
                                        outs = outs,  # to recycle
                                        outs_P_prev = outs_P_prev,  # to recycle
                                        outs_P_curr = outs_P_curr,  # to recycle
                                        outs_P_succ = outs_P_succ,  # to recycle
                                        dtype = dtype)
        self.outs_P_prev, self.outs_P_curr, self.outs_P_succ = geg_out[1:]
        return geg_out[0]
