
▸ ChebyshevBase
-----
**declaration**

```python
    class ChebyshevBase(_polynomial_base): 
```


placeholder



-----
▹ ChebyshevBase.zeros
-----

**declaration**

```python
    @classmethod 
    def zeros(cls, degree: int, dim: int = 1, domain: tuple[float, float] = (-1.0, 1.0)) -> 'ChebyshevBase': 
```


pseudo-constructor



-----

▹ ChebyshevBase.\_\_init\_\_
-----

**declaration**

```python
    def __init__(self, coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None, domain: tuple[float, float] = (-1.0, 1.0)): 
```


placeholder



-----

▹ ChebyshevBase.transform\_t\_arg
-----

**declaration**

```python
    def transform_t_arg(self, t_arg): 
```



-----

▹ ChebyshevBase.\_\_call\_\_
-----

**declaration**

```python
    def __call__(self, t_arg: floatish_T, cap_order_4_diff: Optional[int] = None, outs: Optional[ndarray_T[floatish_T]] = None, outs_P_prev: Optional[ndarray_T[floatish_T]] = None, outs_P_curr: Optional[ndarray_T[floatish_T]] = None, outs_P_succ: Optional[ndarray_T[floatish_T]] = None, dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]: 
```


placeholder



-----
