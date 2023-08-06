
▸ \_polynomial\_base
-----
**declaration**

```python
    class _polynomial_base(metaclass = ABCMeta): 
```


abstract base class for all polynomial bases



-----
▹ \_polynomial\_base.zeros
-----

**declaration**

```python
    @classmethod 
    @abstractmethod 
    def zeros(cls, degree: int, dim: int = 1) -> '_polynomial_base': 
```


create zero polynom

**args**

  - degree: degree or order of polynomial
  - dim: range/output dimension

**returns**

  - instance of class, i.e. a polynomial



-----

▹ \_polynomial\_base.\_\_init\_\_
-----

**declaration**

```python
    def __init__(self, coeff: Optional[Union[ndarray_T[floatish_T], Sequence[floatish_T]]] = None): 
```



-----

▹ \_polynomial\_base.coeff
-----

**declaration**

```python
    @property 
    def coeff(self) -> Union[None, ndarray_T[floatish_T]]: 
```



-----

▹ \_polynomial\_base.coeff
-----

**declaration**

```python
    @coeff.setter 
    def coeff(self, _coeff: Union[None, ndarray_T[floatish_T], Sequence[floatish_T]]): 
```



-----

▹ \_polynomial\_base.degree
-----

**declaration**

```python
    @property 
    def degree(self) -> int: 
```


degree of polynomial

**returns**

  the degree/order of polynomial



-----

▹ \_polynomial\_base.deg
-----

**declaration**

```python
    @property 
    def deg(self) -> int: 
```


degree of polynomial (shorthand for degree)

**returns**

  the degree/order of polynomial



-----

▹ \_polynomial\_base.dim
-----

**declaration**

```python
    @property 
    def dim(self) -> int: 
```


dimension of output

**returns**

  the range/output dimension



-----

▹ \_polynomial\_base.\_\_call\_\_
-----

**declaration**

```python
    @abstractmethod 
    def __call__(self, t_arg: floatish_T, cap_degree_4_eval: Optional[int] = None) -> ndarray_T[floatish_T]: 
```



-----

▸ \_polynomial\_base\_with\_t\_ref
-----
**declaration**

```python
    class _polynomial_base_with_t_ref(_polynomial_base): 
```



-----
▹ \_polynomial\_base\_with\_t\_ref.t\_ref
-----

**declaration**

```python
    @property 
    @abstractmethod 
    def t_ref(self) -> Union[None, floatish_T, ndarray_T[floatish_T]]: 
```



-----

▹ \_polynomial\_base\_with\_t\_ref.t\_ref
-----

**declaration**

```python
    @t_ref.setter 
    @abstractmethod 
    def t_ref(self, _t_ref: Union[None, floatish_T, Sequence[floatish_T], ndarray_T[floatish_T]]): 
```



-----
