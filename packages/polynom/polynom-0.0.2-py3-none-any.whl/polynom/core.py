import numpy as np
import numpy.typing as npt
from abc import ABCMeta, abstractmethod, abstractproperty, abstractstaticmethod
from collections.abc import Sequence
from typing import Union, Optional, Any


floatish_T = Union[Any, float]  # i.e. float or "like a float", e.g. a user defined classes, decimal.Decimal, ...
scalar_or_sequence_or_floatish_T = Union[floatish_T, Sequence[floatish_T]]
ndarray_T = npt.NDArray


def horner(coeff: ndarray_T[floatish_T],
           t_ref: scalar_or_sequence_or_floatish_T,
           t_arg: scalar_or_sequence_or_floatish_T,
           cap_degree_4_eval: Optional[int] = None,
           cap_order_4_diff: Optional[int] = None,
           outs: Optional = None,  # to recycle
           dtype: Optional[np.dtype] = None) -> ndarray_T[floatish_T]:
    order = coeff.shape[1] - 1

    is_newton_base: bool = False
    if hasattr(t_ref, '__getitem__'):
        is_newton_base = True

    t_arg = np.array(t_arg, copy=False)
    if len(t_arg.shape) == 0:
        t_arg = t_arg.reshape((-1,))
    shape_arg = t_arg.shape

    if cap_degree_4_eval is None:
        cap_degree_4_eval = order
    elif cap_degree_4_eval < 0:
        cap_degree_4_eval += order
    else:
        cap_degree_4_eval = min(order, cap_degree_4_eval)

    if cap_order_4_diff is None:
        cap_order_4_diff = 0
    elif cap_order_4_diff < 0:
        cap_order_4_diff += order
    else:
        cap_order_4_diff = min(order, cap_order_4_diff)

    if outs is None:
        if dtype is None:
            dtype = coeff.dtype
        outs = np.empty(shape=(cap_order_4_diff + 1,) + shape_arg, dtype=dtype)
        outs[...] = 0.0
    else:
        if isinstance(outs, Sequence):
            outs = np.array(outs, copy=False)
        if (outs.shape[0] != cap_order_4_diff + 1) or (outs.shape[1:] != shape_arg):
            raise AssertionError(f'outs.shape = {outs.shape} != {(cap_order_4_diff + 1,) + shape_arg}')

    delta_t: Optional[ndarray_T] = None
    if not is_newton_base:
        delta_t = t_arg - t_ref
    for i in range(cap_degree_4_eval, -1, -1):
        if is_newton_base:
            delta_t = t_arg - t_ref[i]
        for j in range(cap_order_4_diff, 0, -1):
            outs[j, ...] = j*outs[j - 1, ...] + delta_t*outs[j, ...]
        outs[0, ...] = coeff[:, i] + delta_t*outs[0, ...]

    return outs


class _polynomial_base(metaclass=ABCMeta):
    _coeff: Union[None, ndarray_T[floatish_T]] = None
    _t_ref: Union[None, floatish_T, ndarray_T[floatish_T]] = None

    @classmethod
    @abstractmethod
    def zeros(cls, degree: int, dim: int = 1) -> '_polynomial_base':
        pass

    def __init__(self, coeff: Optional[Union[ndarray_T[floatish_T], Sequence[floatish_T]]] = None):
        self.coeff = coeff

    @property
    def coeff(self) -> Union[None, ndarray_T[floatish_T]]:
        return self._coeff

    @coeff.setter
    def coeff(self, _coeff: Union[None, ndarray_T[floatish_T], Sequence[floatish_T]]):
        if _coeff is None:
            self._coeff = None
        else:
            if isinstance(_coeff, Sequence):
                _coeff = np.array(_coeff, copy=False)
            if len(_coeff.shape) != 2:
                if len(_coeff.shape) == 1:
                    _coeff = _coeff.reshape((1, -1))
                else:
                    raise AssertionError("shape of coeff has to be: 1 <= len(coeff.shape) <= 2!")
            self._coeff = _coeff

    @property
    @abstractmethod
    def t_ref(self) -> Union[None, floatish_T, ndarray_T[floatish_T]]:
        pass

    @t_ref.setter
    @abstractmethod
    def t_ref(self, _t_ref: Union[None, floatish_T, Sequence[floatish_T], ndarray_T[floatish_T]]):
        pass

    @property
    def degree(self) -> int:
        """
        degree of polynomial in monomial base

        Returns
        -------
            int
                the degree
        """
        if self.coeff is None:
            return -1
        return self.coeff.shape[1] - 1

    @property
    def deg(self) -> int:
        return self.degree

    @property
    def dim(self) -> int:
        """
        (output or range) dimension of polynomial in monomial base

        Returns
        -------
            int
                the dimension
        """
        if self.coeff is None:
            return -1
        return self.coeff.shape[0]

    @abstractmethod
    def __call__(self,
                 t_arg: floatish_T,
                 cap_degree_4_eval: Optional[int] = None) -> ndarray_T[floatish_T]:
        pass


class Monomial(_polynomial_base):
    """
    monomial

    represents polynomials in monomial base representation and uses Horner to evaluate and differentiate;
    polynomials in monomial base can be represented mathematically as:

        p(t) = coeff[:, 0] + coeff[:, 1]*(t - t_ref) + ... + coeff[:, deg]*(t - t_ref)**deg
    """

    @classmethod
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[floatish_T] = 0.0) -> 'Monomial':
        """
        pseudo-constructor to prepare polynomial initialised with zeros only

        Parameters
        ----------
        degree: int
            degree of the polynomial
        dim: int, default = 1
            dimension of the polynomial
        t_ref: Optional[floatish_T], default = 0.0
            reference point

        Returns
        -------
            monomial
        """
        return cls(coeff=np.zeros(shape=(dim, degree + 1)), t_ref=t_ref)

    def __init__(self,
                 coeff: Optional[Union[ndarray_T[floatish_T], Sequence[floatish_T]]] = None,
                 t_ref: Optional[floatish_T] = 0.0):
        """
        constructor of monomial class

        Parameters
        ----------
        coeff: Optional[ndarray_T[floatish_T]], default = None
            1-dim or 2-dim array of coefficients of (potentially vectorized) polynomial (daefault is None)
        t_ref: Optional[floatish_T], default = 0.0
            reference point
        """
        super().__init__(coeff=coeff)
        self.t_ref = t_ref

    @property
    def t_ref(self) -> Union[None, floatish_T]:
        return self._t_ref

    @t_ref.setter
    def t_ref(self, _t_ref: Union[None, floatish_T]):
        self._t_ref = _t_ref

    def __call__(self,
                 t_arg: floatish_T,
                 cap_degree_4_eval: Optional[int] = None,
                 cap_order_4_diff: Optional[int] = None,
                 dtype: Optional[np.dtype] = None) -> ndarray_T[floatish_T]:
        return horner(coeff=self.coeff,
                      t_ref=self.t_ref,
                      t_arg=t_arg,
                      cap_degree_4_eval=cap_degree_4_eval,
                      cap_order_4_diff=cap_order_4_diff,
                      dtype=dtype)


class NewtonBase(_polynomial_base):
    """
    NewtonBase

    represents polynomials in Newton base representation and uses Horner to evaluate and differentiate;
    polynomials in Newton base can be represented mathematically as:

        p(t) = coeff[:, 0] + coeff[:, 1]*(t - t_ref[0]) + coeff[:, 2]*(t - t_ref[0])*(t - t_ref[1]) + ...
    """

    @classmethod
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[ndarray_T[floatish_T]] = None) -> 'NewtonBase':
        """
        pseudo-constructor to prepare polynomial initialised with zeros only

        Parameters
        ----------
        degree: int
            degree of the polynomial
        dim: int, default = 1
            dimension of the polynomial
        t_ref: Optional[floatish_T], default = 0.0
            reference points

        Returns
        -------
        monomial
        """
        return cls(coeff=np.zeros(shape=(dim, degree + 1)), t_ref=t_ref)

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
        super().__init__(coeff=coeff)
        self.t_ref = t_ref

    @property
    def t_ref(self) -> Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]:
        return self._t_ref

    @t_ref.setter
    def t_ref(self, _t_ref: Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]):
        if _t_ref is None:
            self._t_ref = None
        else:
            if isinstance(_t_ref, Sequence):
                _t_ref = np.array(_t_ref, copy=False)
            if len(_t_ref.shape) != 1:
                raise AssertionError("shape of t_ref has to be: len(t_ref.shape) == 1!")
            self._t_ref = _t_ref

    def __call__(self,
                 t_arg: floatish_T,
                 cap_degree_4_eval: Optional[int] = None,
                 cap_order_4_diff: Optional[int] = None,
                 dtype: Optional[np.dtype] = None) -> ndarray_T[floatish_T]:
        return horner(coeff=self.coeff,
                      t_ref=self.t_ref,
                      t_arg=t_arg,
                      cap_degree_4_eval=cap_degree_4_eval,
                      cap_order_4_diff=cap_order_4_diff,
                      dtype=dtype)
