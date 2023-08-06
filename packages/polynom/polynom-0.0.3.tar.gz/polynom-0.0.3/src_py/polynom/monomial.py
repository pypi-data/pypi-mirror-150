from ._base import floatish_T, scalar_or_sequence_or_floatish_T, ndarray_T, dtype_T
from ._base import _polynomial_base_with_t_ref, arr_zeros_constructor

from .shared import horner

from collections.abc import Sequence
from typing import Union, Optional


class MonomialBase(_polynomial_base_with_t_ref):
    """
    **a class representing polynomials in monomial base representation**

    represents polynomials in monomial base representation and uses Horner's method to _evaluate_ and _differentiate_,
    i.e. polynomials are computed via

    $$
    p(t) = c_0 + \delta t\cdot(c_1 + \delta t\cdot (\dots + \delta t\cdot(c_{d-1} + \delta t\cdot c_d) \dots ))
    $$

    and are also algorithmically differentiated from this representation, where $c_i = p.\mathrm{coeff}[:, i]$,
    $d = p.\mathrm{degree}$ as well as $\delta t = t - \mathring t$,
    with $\mathring t = p.\mathrm{t\_ref}$.

    A more readable as well as mathematically equivalent way of representation is:

    $$
    p(t) = \sum_{i=0}^d c_i\cdot\delta t^i
    $$
    """

    @classmethod
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[floatish_T] = 0.0) -> 'MonomialBase':
        """
        pseudo-constructor (or "factory method")

        for the initial preparation of polynomials with :math:`\verb|p.coeff|` initialized as zeros for subsequent
        manipulation;
        final zero-ed ceoff array will have shape = (dim, 1 + degree)

        **args**

            - degree: degree/order of the polynomial
            - dim (default = 1): range/output dimension (in regards of vectorization)
            - t_ref: (default = 0.0): reference point for the polynomial representation

        **returns**

            - constant zero-polynom (but with coeff-vector ready to become an order d polynomial)
        """
        return cls(coeff = arr_zeros_constructor(shape = (dim, degree + 1)), t_ref = t_ref)

    def __init__(self,
                 coeff: Optional[Union[ndarray_T[floatish_T], Sequence[floatish_T]]] = None,
                 t_ref: Optional[floatish_T] = 0.0):
        """
        main-constructor (or "init method")

        **args**

            - coeff (default = None): 1-dim or 2-dim array of coefficients of (potentially vectorized) polynomial;
              if chosen as None then it stays None until assigned by hand
            - t_ref (default = 0.0): reference point for the polynomial representation
        """
        super().__init__(coeff = coeff)
        self.t_ref = t_ref

    @property
    def t_ref(self) -> Union[None, floatish_T]:
        """
        _getter method_

        reference point 't_ref' of the polynomial for shifting argument $\delta t = t - \mathring t$, where
        $\mathring t$ = t_ref

        **returns**

            - t_ref
        """
        return self._t_ref

    @t_ref.setter
    def t_ref(self, new_t_ref: Union[None, floatish_T]):
        """
        _setter method_

        reference point 't_ref' of the polynomial for shifting argument $\delta t = t - \mathring t$, where
        $\mathring t$ = t_ref

        **args**

            - new_t_ref
        """
        self._t_ref = new_t_ref

    def __call__(self,
                 t_arg: floatish_T,
                 cap_degree_4_eval: Optional[int] = None,
                 cap_order_4_diff: Optional[int] = None,
                 outs: Optional = None,
                 dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]:
        """
        call function (also for differentiation) of polynomial

        exploits heavily on Hornor's method to evaluate but also differentiate the encoded polynomial up
        to any differentiation order.
        Furthermore, allows to cap the evaluation,
        i.e. let $\gamma = \mathrm{cap\_degree\_4\_eval} \le d = p.\mathrm{degree}$ then this function evaluates
        (and also differentiaties) the equivalent expression

        $$
        \bar p(t) = \sum_{i=0}^{\gamma} c_i \delta t^i,
        $$

        i.e. skipping the last $p(t) - \bar p(t) = \sum_{i=\gamma + 1}^d c_i \delta t^i$ summands. <br>
        Note that \(\delta t = t - \mathring t\), with \(t = \mathrm{t\_arg}\) and \(\mathring t = p.\mathrm{t\_ref}\).

        If $\mathrm{cap\_degree\_4\_eval} < 0$ then $\gamma = \mathrm{cap\_degree\_4\_eval} + p.\mathrm{degree}$.

        **args**

            - t_arg: argument \(t = \mathrm{t\_arg}\) and part of $\delta t = t - \mathring t$, where
              \(t = \mathrm{t\_arg}\) and \(\mathring t = p.\mathrm{t\_ref}\)
            - cap_degree_4_eval (default = None (i.e. no cap)): the degree cap or \(\gamma\) for the evaluation;
              may range from $-p.\mathrm{degree}$ to $p.\mathrm{degree}$
            - cap_order_4_diff (default = None (i.e. no differentiation)): the order cap for differentiation.
              If int then all derivatives up to and including cap_order_4_diff will be computed
            - dtype (default = None (i.e. determined from $p.\mathrm{coeff}$)): for choosing the dtype
              (in the meaning of np == numpy) of the result (usefull when using instances of self defined classes)

        **returns**

            - result array out of shape = (1 + cap_order_4_diff, t_arg.shape); if cap_order_4_diff was chosen None,
              then it is treated as cap_order_4_diff = 0. <br>
              primal evaluation is encoded as $p(t) = \mathrm{out[0, \dots]}$, whereas the j-th derivative
              is encoded as $\tfrac{d^j}{d t^j}\, p(t) = \mathrm{out[j, \dots]}$
        """
        return horner(coeff = self.coeff,
                      t_ref = self.t_ref,
                      t_arg = t_arg,
                      is_newton_base = False,
                      cap_degree_4_eval = cap_degree_4_eval,
                      cap_order_4_diff = cap_order_4_diff,
                      outs = outs,
                      dtype = dtype)
