# Metaclasses and singleton

## metaclass

```python
class SingletonMeta(type):
    _instance = None
    
    def __call__(self, *args, **kwargs):
        if not Singleton._instance:
            Singleton._instance = type.__call__(self, *args, **kwargs)
        return Singleton._instance

class Singleton(metaclass = SingletonMeta):
    pass
```

## Use `__new__`

```python
class A:
    _instnace = None
    
    def __new__(cls, *args, **kwargs):
        if not A._instance:
            A._instance = super().__new__(cls)
        return A._instance
    
    def __init__(self, a):
        pass
```

需要理解的是当我们instantiate的时候，参数会同时传给`__new__` 和 `__init__`

就像：

```python
self = class.__new__(*args, **kwargs)
self.__init__(*args, **kwargs)
```

