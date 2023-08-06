# SmartParams

SmartParams is a lightweight Python framework that simplifies configuration of research projects.
Creates an abstraction that warp configurable classes and extracts from them the necessary
parameters into a configuration file and then injects them initialization. SmartParams can be easily
integrated into existing projects, even if they are very complex. Takes care of loading the
configuration file from path given in code or via command line.

# Installation

#### Requirements

* Python >= 3.8

\
Install via [PyPI](https://pypi.org/project/SmartParams/) &nbsp; `pip install SmartParams`.

# What is Smart class

_Smart_ class is like as _partial_ from _functools_ but only for classes.
_Smart_ object called will instantiate class called with the args and kwargs. If more arguments are
supplied to the call, they are merged with initial keyword arguments.

```python
from smartparams import Smart


class SomeClass:
    def __init__(self, a: str, b: str) -> None:
        print(f"Init SomeClass({a=}, {b=})")


smart_some_class = Smart(SomeClass, a="a")
some_class_object = smart_some_class(b="b")
```

### Key features:

* Wraps class to be partially or fully configurable.
* Allows setting attributes that depend on other objects.
* Creates a configuration template file based on class dependencies in the program.
* Loads configuration from yaml.
* Checks unset parameters.
* Checks the type of parameters.
* Allows overriding configuration from command line.

# Basic usage

Assume that we have _Class_ which expects name and class _Random_.
_Random_ expects an integer value which, if not specified, is set randomly from 1 to 100.
(The full script can be found in the `examples/basic/script.py`).

```python
class Random:
    def __init__(self, value: int = 0) -> None:
        self.value = value or randint(1, 100)
        print(f"Init {self}")

    def __repr__(self) -> str:
        return f"Random({self.value=})"


class Class:
    def __init__(self, name: str, random: Random) -> None:
        self.name = name
        self.random = random
        print(f"Init {self}")

    def __repr__(self) -> str:
        return f"Class({self.name=}, {self.random=})"
```

Our program requires _Class_ with positive random value and another _Class_ with value that is its
negative. First, create dataclass with smart classes, then in post_init setup _Smart[Class]_
objects.

```python
@dataclass
class Params:
    positive_class: Smart[Class]
    negative_class: Smart[Class]

    def __post_init__(self) -> None:
        random = self.positive_class.init('random')
        self.negative_class.set('random.value', random.value * -1)
        self.message = self.positive_class.pop('message')
        self.positive_class.map('name', str.upper)
```

Define main function that expects _Smart[Class]_ object.

```python
def main(smart: Smart[Params]) -> None:
    print("--- Configure Params")
    params = smart()

    print("\n--- Configure PositiveClass")
    params.positive_class()

    print("\n--- Configure NegativeClass")
    params.negative_class(name="negative_class")

    print("\n--- " + params.message)
```

Create script runner that add abstract for cli and load config file from given path.

```python
if __name__ == '__main__':
    Smart(Params).run(
        function=main,
        path=Path('examples/basic/params.yaml'),
    )
```

Before running the script, create a params template file with \
`python -m examples.basic.script --dump`, \
then edit this file (`examples/basic/params.yaml`) and set the appropriate values.

```yaml
positive_class:
  class: __main__.Class:Smart
  name: "positive_class"
  message: "Hello SmartWorld!"
  random:
    class: __main__.Random

negative_class:
  class: __main__.Class:Smart
  random:
    class: __main__.Random
```

Finally, run script `python -m examples.basic.script`, optionally modify parameters via cli \
by adding `positive_class.name="very_positive_class"` to command. \
For more options use `--help` argument.

# Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/),
please ensure the coverage at least stays the same before you submit a merge request.

# License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license,
"SmartParams" is free and open source software.

# Issues

If you encounter any problems, please email us at <mateusz.baran.sanok@gmail.com>, along with a
detailed description.
