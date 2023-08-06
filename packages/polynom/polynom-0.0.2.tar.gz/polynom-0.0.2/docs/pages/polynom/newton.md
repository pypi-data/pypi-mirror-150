
▸ NewtonBase
-----
**declaration**

```python
    class NewtonBase(_polynomial_base_with_t_ref): 
```


NewtonBase

represents polynomials in Newton base representation and uses Horner to evaluate and differentiate;
polynomials in Newton base can be represented mathematically as:

  p(t) = coeff[:, 0] + coeff[:, 1]*(t - t_ref[0]) + coeff[:, 2]*(t - t_ref[0])*(t - t_ref[1]) + ...



-----
▹ NewtonBase.zeros
-----

**declaration**

```python
    @classmethod 
    def zeros(cls, degree: int, dim: int = 1, t_ref: Optional[ndarray_T[floatish_T]] = None) -> 'NewtonBase': 
```


pseudo-constructor



-----

▹ NewtonBase.\_\_init\_\_
-----

**declaration**

```python
    def __init__(self, coeff: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None, t_ref: Optional[Union[Sequence[floatish_T], ndarray_T[floatish_T]]] = None): 
```


constructor of monomial class

Parameters
----------
coeff: Optional[ndarray_T[floatish_T]], default = None
  1-dim or 2-dim array of coefficients of (potentially vectorized) polynomial (daefault is None)
t_ref: Optional[floatish_T], default = 0.0
  reference points



-----

▹ NewtonBase.t\_ref
-----

**declaration**

```python
    @property 
    def t_ref(self) -> Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]: 
```


placeholder



-----

▹ NewtonBase.t\_ref
-----

**declaration**

```python
    @t_ref.setter 
    def t_ref(self, _t_ref: Union[None, Sequence[floatish_T], ndarray_T[floatish_T]]): 
```



-----

▹ NewtonBase.\_\_call\_\_
-----

**declaration**

```python
    def __call__(self, t_arg: floatish_T, cap_order_4_diff: Optional[int] = None, outs: Optional = None, dtype: Optional[dtype_T] = None) -> ndarray_T[floatish_T]: 
```


placeholder



-----
