
\_check\_or\_init\_outs
-----

**declaration**

```python
    def _check_or_init_outs(shape_arg: tuple[int], cap_order_4_diff: int, outs: Optional[ndarray_T[floatish_T]], coeff: Optional[ndarray_T[floatish_T]] = None, dtype: Optional[dtype_T] = None): 
```



-----

\_get\_\_order
-----

**declaration**

```python
    def _get__order(coeff: ndarray_T[floatish_T]) -> int: 
```



-----

\_get\_t\_arg\_and\_shape
-----

**declaration**

```python
    def _get_t_arg_and_shape(t_arg: ndarray_T[floatish_T]) -> tuple[ndarray_T[floatish_T], tuple[int, ...]]: 
```



-----

\_filter\_cap
-----

**declaration**

```python
    def _filter_cap(cap: Optional[int], offset: int, default: int) -> int: 
```



-----

horner
-----

**declaration**

```python
    def horner(coeff: ndarray_T[floatish_T], t_ref: ndarray_T[floatish_T], t_arg: ndarray_T[floatish_T], is_newton_base: bool, cap_degree_4_eval: Optional[int] = None, cap_order_4_diff: Optional[int] = None, outs: Optional[ndarray_T[floatish_T]] = None, dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]: 
```


placeholder



-----

lagrange\_basis\_func
-----

**declaration**

```python
    def lagrange_basis_func(i: int, order: int, t_arg: ndarray_T[floatish_T], t_ref: ndarray_T[floatish_T], dtype: dtype_T, cap_order_4_diff: Optional[int] = None, outs: Optional[ndarray_T[floatish_T]] = None) -> ndarray_T[floatish_T]:  # to recycle 
```


placeholder



-----

lagrange\_poly\_eval
-----

**declaration**

```python
    def lagrange_poly_eval(coeff: ndarray_T[floatish_T], t_ref: ndarray_T[floatish_T], t_arg: ndarray_T[floatish_T], cap_order_4_diff: Optional[int] = None, outs: Optional[ndarray_T[floatish_T]] = None, outs_lagrange_basis: Optional[ndarray_T[floatish_T]] = None, dtype: Optional[dtype_T] = None) -> tuple[ndarray_T[floatish_T], ndarray_T[floatish_T]]: 
```


placeholder



-----

gegenbauer\_gen
-----

**declaration**

```python
    def gegenbauer_gen(alpha: floatish_T): 
```



-----

gegenbauer\_rec
-----

**declaration**

```python
    def gegenbauer_rec(P_succ: ndarray_T[floatish_T], P_curr: ndarray_T[floatish_T], P_prev: ndarray_T[floatish_T], n: int, t_arg: ndarray_T[floatish_T], d_t_arg: ndarray_T[floatish_T], cap_order_4_diff: int) -> ndarray_T[floatish_T]: 
```


placeholder



-----

gegenbauer\_eval
-----

**declaration**

```python
    def gegenbauer_eval(coeff: ndarray_T[floatish_T], t_arg: ndarray_T[floatish_T], d_t_arg: ndarray_T[floatish_T], cap_order_4_diff: Optional[int] = None, outs: Optional[ndarray_T[floatish_T]] = None, outs_P_prev: Optional[ndarray_T[floatish_T]] = None, outs_P_curr: Optional[ndarray_T[floatish_T]] = None, outs_P_succ: Optional[ndarray_T[floatish_T]] = None, dtype: Optional[dtype_T] = None) -> tuple[ndarray_T[floatish_T], ndarray_T[floatish_T], ndarray_T[floatish_T], ndarray_T[floatish_T]]: 
```


placeholder



-----
