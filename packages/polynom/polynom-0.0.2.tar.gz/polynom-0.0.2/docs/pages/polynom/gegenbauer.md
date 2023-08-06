
▸ GegenbauerBase
-----
**declaration**

```python
    class GegenbauerBase(_polynomial_base): 
```


placeholder



-----
▹ GegenbauerBase.zeros
-----

**declaration**

```python
    @classmethod 
    def zeros(cls, alpha: floatish_T, degree: int, dim: int = 1, domain: tuple[float, float] = (-1.0, 1.0)) -> 'GegenbauerBase': 
```


pseudo-constructor



-----

▹ GegenbauerBase.\_\_init\_\_
-----

**declaration**

```python
    def __init__(self, alpha: floatish_T, coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None, domain: tuple[float, float] = (-1.0, 1.0)): 
```


placeholder



-----

▹ GegenbauerBase.alpha
-----

**declaration**

```python
    @property 
    def alpha(self): return self._alpha @alpha.setter def alpha(self, new_alpha: floatish_T): 
```



-----

▹ GegenbauerBase.transform\_t\_arg
-----

**declaration**

```python
    def transform_t_arg(self, t_arg): 
```



-----

▹ GegenbauerBase.\_\_call\_\_
-----

**declaration**

```python
    def __call__(self, t_arg: floatish_T, cap_order_4_diff: Optional[int] = None, outs: Optional[ndarray_T[floatish_T]] = None, outs_P_prev: Optional[ndarray_T[floatish_T]] = None, outs_P_curr: Optional[ndarray_T[floatish_T]] = None, outs_P_succ: Optional[ndarray_T[floatish_T]] = None, dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]: 
```


placeholder



-----
