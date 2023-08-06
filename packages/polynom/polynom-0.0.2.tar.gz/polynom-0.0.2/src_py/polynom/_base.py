import numpy as np
import numpy.typing as npt
from abc import ABCMeta, abstractmethod, abstractproperty, abstractstaticmethod
from collections.abc import Sequence
from typing import Union, Optional, Any


floatish_T = Union[Any, float]  # i.e. float or "like a float", e.g. a user defined classes, decimal.Decimal, ...
scalar_or_sequence_or_floatish_T = Union[floatish_T, Sequence[floatish_T]]
ndarray_T = npt.NDArray
dtype_T = np.dtype


arr_constructor = np.array
arr_empty_contructor = np.empty
arr_zeros_constructor = np.zeros
arr_ones_constructor = np.ones


class _polynomial_base(metaclass = ABCMeta):
    '''
    abstract base class for all polynomial bases
    '''
    _coeff: Union[None, ndarray_T[floatish_T]] = None
    _t_ref: Union[None, floatish_T, ndarray_T[floatish_T]] = None

    @classmethod
    @abstractmethod
    def zeros(cls, degree: int, dim: int = 1) -> '_polynomial_base':
        '''
        create zero polynom

        **args**

            - degree: degree or order of polynomial
            - dim: range/output dimension

        **returns**

            - instance of class, i.e. a polynomial
        '''
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
                _coeff = np.array(_coeff, copy = False)
            if len(_coeff.shape) != 2:
                if len(_coeff.shape) == 1:
                    _coeff = _coeff.reshape((1, -1))
                else:
                    raise AssertionError("shape of coeff has to be: 1 <= len(coeff.shape) <= 2!")
            self._coeff = _coeff

    @property
    def degree(self) -> int:
        """
        degree of polynomial

        **returns**

            the degree/order of polynomial
        """
        if self.coeff is None:
            return -1
        return self.coeff.shape[1] - 1

    @property
    def deg(self) -> int:
        """
        degree of polynomial (shorthand for degree)

        **returns**

            the degree/order of polynomial
        """
        return self.degree

    @property
    def dim(self) -> int:
        """
        dimension of output

        **returns**

            the range/output dimension
        """
        if self.coeff is None:
            return -1
        return self.coeff.shape[0]

    @abstractmethod
    def __call__(self,
                 t_arg: floatish_T,
                 cap_degree_4_eval: Optional[int] = None) -> ndarray_T[floatish_T]:
        pass


class _polynomial_base_with_t_ref(_polynomial_base):

    @property
    @abstractmethod
    def t_ref(self) -> Union[None, floatish_T, ndarray_T[floatish_T]]:
        pass

    @t_ref.setter
    @abstractmethod
    def t_ref(self, _t_ref: Union[None, floatish_T, Sequence[floatish_T], ndarray_T[floatish_T]]):
        pass
