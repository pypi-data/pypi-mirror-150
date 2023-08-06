
▸ LagrangeBase
-----
**declaration**

```python
    class LagrangeBase(_polynomial_base_with_t_ref): 
```


placeholder



-----
▹ LagrangeBase.zeros
-----

**declaration**

```python
    @classmethod 
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[ndarray_T[floatish_T]] = None) -> 'LagrangeBase': 
```


pseudo-constructor



-----

▹ LagrangeBase.\_\_init\_\_
-----

**declaration**

```python
    def __init__(self, coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None, t_ref: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None): 
```


placeholder



-----

▹ LagrangeBase.t\_ref
-----

**declaration**

```python
    @property 
    def t_ref(self) -> Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]: 
```


placeholder



-----

▹ LagrangeBase.t\_ref
-----

**declaration**

```python
    @t_ref.setter 
    def t_ref(self, _t_ref: Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]): 
```



-----

▹ LagrangeBase.\_\_call\_\_
-----

**declaration**

```python
    def __call__(self, t_arg: floatish_T, cap_order_4_diff: Optional[int] = None, outs: Optional = None, outs_lagrange_basis: Optional = None, dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]: 
```



-----
