
# Mapping Shortcuts

python package with useful mapping shortcuts

## Contains  

 - Decorator for mapping factory
 - Metaclass for mapping factory
 - Function for import all subpackages in package  

### Decorator factory for mapping

```python

from mapping_shortcuts.decors import create_collector

decorator, collection = create_collector(
    raise_on_duplicate=True,  # default: True
)

@decorator('key1')
def func1():
    ...

@decorator('key2')
def func2():
    ...

print(collection) 
'''
output: {
    'key1': <function func1 at 0x104adc430>,
    'key2': <function func2 at 0x104adc4c0>,
}
'''

```

### Metaclass factory for mapping

```python
import abc
from mapping_shortcuts.meta import create_collection_meta

MetaClass, collections = create_collection_meta(
    base=abc.ABCMeta,  # default: type
    getter=lambda x: x.__name__,  # default: lambda x: str(x)
    raise_on_duplicate = True,  # default: True
)


class A(metaclass=MetaClass):
    ...

class B(metaclass=MetaClass):
    ...

print(collections)
'''
oputput: {
    'A': <class '__main__.A'>,
    'B': <class '__main__.B'>,
}
'''
```

### Function for import all subpackages in package

For exmaple with have five files:
- python code `app/tools.py`
- empty file `app/providers/a/__init__.py`
- empty file `app/providers/b/__init__.py`
- python code in `app/providers/a/module.py`
- python code in`app/providers/b/module.py`

`app/tools.py` be like:

```python
from mapping_shortcuts.decors import create_collector

decorator, collection = create_collector()
```

`app/providers/a/module.py` is: 
```python
from app.tools import decorator

@decorator('A-func')
def function_a():
    ...
```

`app/providers/b/module.py` is: 
```python
from app.tools import decorator

@decorator('B-func')
def function_b():
    ...
```

execute `load_package()`:
```python

from mapping_shortcuts.dirtools import load_package
from app.tools import collection

load_package('app.providers')
print(collection)
'''
output: {
    'A-func': <function function_a at 0x104cfa0e0>,
    'B-func': <function function_b at 0x104cfa290>,
}
'''
```