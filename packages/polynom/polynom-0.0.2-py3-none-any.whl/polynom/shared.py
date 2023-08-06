from ._base import floatish_T, scalar_or_sequence_or_floatish_T, ndarray_T, dtype_T
from ._base import arr_constructor, arr_empty_contructor

from collections.abc import Sequence
from typing import Optional, Union


def _check_or_init_outs(shape_arg: tuple[int],
                        cap_order_4_diff: int,
                        outs: Optional[ndarray_T[floatish_T]],
                        coeff: Optional[ndarray_T[floatish_T]] = None,
                        dtype: Optional[dtype_T] = None):
    if outs is None:
        if dtype is None:
            if coeff is None: raise AssertionError('dtype and coeff can not be None together!')
            dtype = coeff.dtype
        outs = arr_empty_contructor(shape = (cap_order_4_diff + 1,) + shape_arg, dtype = dtype)
    else:
        if isinstance(outs, Sequence): outs = arr_constructor(outs, copy = False)
        if (outs.shape[0] != cap_order_4_diff + 1) or (outs.shape[1:] != shape_arg):
            raise AssertionError(f'outs.shape = {outs.shape} != {(cap_order_4_diff + 1,) + shape_arg}')
    return outs, outs.dtype


def _get__order(coeff: ndarray_T[floatish_T]) -> int:
    return coeff.shape[1] - 1


def _get_t_arg_and_shape(t_arg: ndarray_T[floatish_T]) -> tuple[ndarray_T[floatish_T], tuple[int, ...]]:
    t_arg = arr_constructor(t_arg, copy = False)
    if len(t_arg.shape) == 0: t_arg = t_arg.reshape((-1,))

    return t_arg, t_arg.shape


def _filter_cap(cap : Optional[int], offset: int, default: int) -> int:
    if cap is None: cap = default
    elif cap < 0: cap += offset
    else: cap = min(offset, cap)
    return cap


def horner(coeff: ndarray_T[floatish_T],
           t_ref: ndarray_T[floatish_T],
           t_arg: ndarray_T[floatish_T],
           is_newton_base: bool,
           cap_degree_4_eval: Optional[int] = None,
           cap_order_4_diff: Optional[int] = None,
           outs: Optional[ndarray_T[floatish_T]] = None,  # to recycle
           dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]:
    """
    placeholder
    """
    order = _get__order(coeff = coeff)
    t_arg, shape_arg = _get_t_arg_and_shape(t_arg = t_arg)

    cap_order_4_diff = _filter_cap(cap = cap_order_4_diff, offset = order, default = 0)
    cap_degree_4_eval = _filter_cap(cap = cap_degree_4_eval, offset = order, default = order)

    outs, _ = _check_or_init_outs(shape_arg = shape_arg,
                                  cap_order_4_diff = cap_order_4_diff,
                                  outs = outs,
                                  coeff = coeff,
                                  dtype = dtype)
    outs[...] = 0.0  # reset outs

    delta_t: Optional[ndarray_T] = None
    if not is_newton_base: delta_t = t_arg - t_ref
    for i in range(cap_degree_4_eval, -1, -1):
        if is_newton_base: delta_t = t_arg - t_ref[i]
        for j in range(cap_order_4_diff, 0, -1): # apply principles of algorithmic differentiation
            outs[j, ...] = j*outs[j - 1, ...] + delta_t*outs[j, ...] # derivatives propagated from high to low order
        outs[0, ...] = coeff[:, i] + delta_t*outs[0, ...] # primal operation

    return outs


def lagrange_basis_func(i: int,
                        order: int,
                        t_arg: ndarray_T[floatish_T],
                        t_ref: ndarray_T[floatish_T],
                        dtype: dtype_T,
                        cap_order_4_diff: Optional[int] = None,
                        outs: Optional[ndarray_T[floatish_T]] = None) -> ndarray_T[floatish_T]:  # to recycle
    """
    placeholder
    """
    shape_arg = t_arg.shape

    outs, _ = _check_or_init_outs(shape_arg = shape_arg,
                                  cap_order_4_diff = cap_order_4_diff,
                                  outs = outs,
                                  dtype = dtype)
    outs[0, ...] = 1.0  # reset outs
    outs[1:, ...] = 0.0  # reset outs; init derivatives, where derivative of outs[0, ...] = 1.0 is 0.0

    t_i = t_ref[i]
    for j in range(order, -1, -1):
        if j == i: continue
        t_j = t_ref[j]
        count = t_arg - t_j  # d_count == 1.0
        denom_inv = 1.0/(t_i - t_j)  # d_denom == 0.0
        frac = count*denom_inv  # d_frac == denom_inv
        for j in range(cap_order_4_diff, 0, -1):  # apply principles of algorithmic differentiation
            outs[j, ...] = j*outs[j - 1, ...]*denom_inv + frac*outs[
                j, ...]  # derivatives propagated from high to low order
        outs[0, ...] = frac*outs[0, ...]

    return outs


def lagrange_poly_eval(coeff: ndarray_T[floatish_T],
                       t_ref: ndarray_T[floatish_T],
                       t_arg: ndarray_T[floatish_T],
                       cap_order_4_diff: Optional[int] = None,
                       outs: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                       outs_lagrange_basis: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                       dtype: Optional[dtype_T] = None) -> tuple[ndarray_T[floatish_T],
                                                                 ndarray_T[floatish_T]]:
    """
    placeholder
    """
    order = _get__order(coeff = coeff)
    t_arg, shape_arg = _get_t_arg_and_shape(t_arg = t_arg)

    cap_order_4_diff = _filter_cap(cap = cap_order_4_diff, offset = order, default = 0)

    outs, dtype = _check_or_init_outs(shape_arg = shape_arg,
                                      cap_order_4_diff = cap_order_4_diff,
                                      outs = outs,
                                      coeff = coeff,
                                      dtype = dtype)
    outs[...] = 0.0  # reset outs

    for i in range(order, -1, -1):
        outs_lagrange_basis = lagrange_basis_func(i = i,
                                                  order = order,
                                                  t_arg = t_arg,
                                                  t_ref = t_ref,
                                                  dtype = dtype,
                                                  cap_order_4_diff = cap_order_4_diff,
                                                  outs = outs_lagrange_basis)
        outs = outs + coeff[:, i]*outs_lagrange_basis

    return outs, outs_lagrange_basis


# def legendre_rec(P_succ: ndarray_T[floatish_T],  # P_succ to recycle
#                  P_curr: ndarray_T[floatish_T],
#                  P_prev: ndarray_T[floatish_T],
#                  n: int,
#                  t_arg: ndarray_T[floatish_T],
#                  d_t_arg: ndarray_T[floatish_T],
#                  cap_order_4_diff: int) -> ndarray_T[floatish_T]:
#     """
#     placeholder
#     """
#     denom: int = n  # copy
#     _n = n - 1.0  # adjust by shift compared to most book definitions
#     coeff: int = _n + denom  # 2.0*n + 1.0  #
#
#     P_succ[...] = 0.0  # reset P_succ
#
#     tmp_curr = t_arg*P_curr[0, ...]
#     for j in range(cap_order_4_diff, 0, -1):
#         dj_tmp_curr = j*d_t_arg*P_curr[j - 1, ...] + t_arg*P_curr[j, ...]  # j-th derivative of tmp_curr
#         P_succ[j, ...] = (coeff*dj_tmp_curr - _n*P_prev[j, ...])/denom
#     P_succ[0, ...] = (coeff*tmp_curr - _n*P_prev[0, ...])/denom
#     return P_succ
#
#
# def legendre_eval(coeff: ndarray_T[floatish_T],
#                   t_arg: ndarray_T[floatish_T],
#                   d_t_arg: ndarray_T[floatish_T],
#                   cap_order_4_diff: Optional[int] = None,
#                   outs: Optional[ndarray_T[floatish_T]] = None,  # to recycle
#                   outs_P_prev: Optional[ndarray_T[floatish_T]] = None,  # to recycle
#                   outs_P_curr: Optional[ndarray_T[floatish_T]] = None,  # to recycle
#                   outs_P_succ: Optional[ndarray_T[floatish_T]] = None,  # to recycle
#                   dtype: Optional[dtype_T] = None) -> tuple[ndarray_T[floatish_T],
#                                                             ndarray_T[floatish_T],
#                                                             ndarray_T[floatish_T],
#                                                             ndarray_T[floatish_T]]:
#     """
#     placeholder
#     """
#     order = _get__order(coeff = coeff)
#     t_arg, shape_arg = _get_t_arg_and_shape(t_arg = t_arg)
#
#     cap_order_4_diff = _filter_cap(cap = cap_order_4_diff, offset = order, default = 0)
#
#     outs, dtype = _check_or_init_outs(shape_arg = shape_arg,
#                                       cap_order_4_diff = cap_order_4_diff,
#                                       outs = outs,
#                                       coeff = coeff,
#                                       dtype = dtype)
#     # outs[...] = 0.0  # reset outs
#     outs_P_prev, _ = _check_or_init_outs(shape_arg = shape_arg,
#                                          cap_order_4_diff = cap_order_4_diff,
#                                          outs = outs_P_prev,
#                                          dtype = dtype)
#     outs_P_prev[0, ...] = 1.0  # reset outs_P_prev
#     outs_P_prev[1:, ...] = 0.0  # reset outs_P_prev
#     outs[:] = coeff[:, 0]*outs_P_prev
#     if order == 0: return outs, outs_P_prev, outs_P_curr, outs_P_succ
#     outs_P_curr, _ = _check_or_init_outs(shape_arg = shape_arg,
#                                          cap_order_4_diff = cap_order_4_diff,
#                                          outs = outs_P_curr,
#                                          dtype = dtype)
#     outs_P_curr[0, ...] = t_arg  # reset outs_P_curr
#     if cap_order_4_diff > 0: outs_P_curr[1, ...] = d_t_arg  # reset outs_P_curr
#     outs_P_curr[2:, ...] = 0.0  # reset outs_P_curr
#     outs = outs + coeff[:, 1]*outs_P_curr
#     if order == 1: return outs, outs_P_prev, outs_P_curr, outs_P_succ
#     outs_P_succ, _ = _check_or_init_outs(shape_arg = shape_arg,
#                                          cap_order_4_diff = cap_order_4_diff,
#                                          outs = outs_P_succ,
#                                          dtype = dtype)
#
#     for n in range(2, order + 1):
#         outs_P_succ = legendre_rec(P_succ = outs_P_succ, P_curr = outs_P_curr, P_prev = outs_P_prev, n = n,
#                                    t_arg = t_arg, d_t_arg = d_t_arg, cap_order_4_diff = cap_order_4_diff)
#         outs = outs + coeff[:, n]*outs_P_succ
#         outs_P_prev, outs_P_curr, outs_P_succ = outs_P_curr, outs_P_succ, outs_P_prev
#
#     return outs, outs_P_prev, outs_P_curr, outs_P_succ


def gegenbauer_gen(alpha:floatish_T):
    def gegenbauer_rec(P_succ: ndarray_T[floatish_T],  # P_succ to recycle
                       P_curr: ndarray_T[floatish_T],
                       P_prev: ndarray_T[floatish_T],
                       n: int,
                       t_arg: ndarray_T[floatish_T],
                       d_t_arg: ndarray_T[floatish_T],
                       cap_order_4_diff: int) -> ndarray_T[floatish_T]:
        """
        placeholder
        """
        coeff: floatish_T = 2.0*(n + alpha - 1.0)

        P_succ[...] = 0.0  # reset P_succ

        tmp_curr = t_arg*P_curr[0, ...]
        for j in range(cap_order_4_diff, 0, -1):
            dj_tmp_curr = j*d_t_arg*P_curr[j - 1, ...] + t_arg*P_curr[j, ...]  # j-th derivative of tmp_curr
            P_succ[j, ...] = (coeff*dj_tmp_curr - (coeff - n)*P_prev[j, ...])  # /n
        P_succ[0, ...] = (coeff*tmp_curr - (coeff - n)*P_prev[0, ...])  # /n
        return P_succ/n

    def gegenbauer_eval(coeff: ndarray_T[floatish_T],
                        t_arg: ndarray_T[floatish_T],
                        d_t_arg: ndarray_T[floatish_T],
                        cap_order_4_diff: Optional[int] = None,
                        outs: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                        outs_P_prev: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                        outs_P_curr: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                        outs_P_succ: Optional[ndarray_T[floatish_T]] = None,  # to recycle
                        dtype: Optional[dtype_T] = None) -> tuple[ndarray_T[floatish_T],
                                                                  ndarray_T[floatish_T],
                                                                  ndarray_T[floatish_T],
                                                                  ndarray_T[floatish_T]]:
        """
        placeholder
        """
        order = _get__order(coeff = coeff)
        t_arg, shape_arg = _get_t_arg_and_shape(t_arg = t_arg)

        cap_order_4_diff = _filter_cap(cap = cap_order_4_diff, offset = order, default = 0)

        outs, dtype = _check_or_init_outs(shape_arg = shape_arg,
                                          cap_order_4_diff = cap_order_4_diff,
                                          outs = outs,
                                          coeff = coeff,
                                          dtype = dtype)
        # outs[...] = 0.0  # reset outs
        outs_P_prev, _ = _check_or_init_outs(shape_arg = shape_arg,
                                             cap_order_4_diff = cap_order_4_diff,
                                             outs = outs_P_prev,
                                             dtype = dtype)
        outs_P_prev[0, ...] = 1.0  # reset outs_P_prev
        outs_P_prev[1:, ...] = 0.0  # reset outs_P_prev
        outs[:] = coeff[:, 0]*outs_P_prev
        if order == 0: return outs, outs_P_prev, outs_P_curr, outs_P_succ
        outs_P_curr, _ = _check_or_init_outs(shape_arg = shape_arg,
                                             cap_order_4_diff = cap_order_4_diff,
                                             outs = outs_P_curr,
                                             dtype = dtype)
        outs_P_curr[0, ...] = 2.0*alpha*t_arg  # reset outs_P_curr
        if cap_order_4_diff > 0: outs_P_curr[1, ...] = 2.0*alpha*d_t_arg  # reset outs_P_curr
        outs_P_curr[2:, ...] = 0.0  # reset outs_P_curr
        outs = outs + coeff[:, 1]*outs_P_curr
        if order == 1: return outs, outs_P_prev, outs_P_curr, outs_P_succ
        outs_P_succ, _ = _check_or_init_outs(shape_arg = shape_arg,
                                             cap_order_4_diff = cap_order_4_diff,
                                             outs = outs_P_succ,
                                             dtype = dtype)

        for n in range(2, order + 1):
            outs_P_succ = gegenbauer_rec(P_succ = outs_P_succ, P_curr = outs_P_curr, P_prev = outs_P_prev, n = n,
                                         t_arg = t_arg, d_t_arg = d_t_arg, cap_order_4_diff = cap_order_4_diff)
            outs = outs + coeff[:, n]*outs_P_succ
            outs_P_prev, outs_P_curr, outs_P_succ = outs_P_curr, outs_P_succ, outs_P_prev

        return outs, outs_P_prev, outs_P_curr, outs_P_succ

    return gegenbauer_eval, gegenbauer_rec


legendre_eval, legendre_rec = gegenbauer_gen(alpha = 0.5)


chebyshev_eval, chebyshev_rec = gegenbauer_gen(alpha = 0.5)  # chebychev-polynomials of 2nd kind
