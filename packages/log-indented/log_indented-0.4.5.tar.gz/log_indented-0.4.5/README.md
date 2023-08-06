
[![Support Ukraine Badge](https://bit.ly/support-ukraine-now)](https://github.com/support-ukraine/support-ukraine#support-financially)

# log-indented

[![Python Package](https://github.com/markmark206/log-indented/actions/workflows/python-publish.yml/badge.svg)](https://github.com/markmark206/log-indented/actions/workflows/python-publish.yml)


This package helps you and your code produce indented, human-friendly, easy to understand logs.


Executing `count_barnyard_animals()` in this code example:

```python
from log_indented import logged, log_info

@logged(logger)
def count_chicken() -> int:
    return 3


@logged(logger)
def count_ducks() -> int:
    return 7


@logged(logger)
def count_birds() -> int:
    return count_chicken() + count_ducks()


@logged(logger)
def count_goats() -> int:
    return 7


@logged(logger)
def count_sheep() -> int:
    return 0


@logged(logger)
def count_barnyard_animals() -> int:
    total_animal_count: int = count_birds() + count_goats() + count_sheep()
    log_info(f"total barnyard animals: {total_animal_count}")
    return total_animal_count
```

will produce output similar to this:

```
    + count_barnyard_animals: enter
        + count_birds: enter
            + count_chicken: enter
            - count_chicken: exit. took 0.00 ms.
            + count_ducks: enter
            - count_ducks: exit. took 0.00 ms.
        - count_birds: exit. took 0.07 ms.
        + count_goats: enter
        - count_goats: exit. took 0.00 ms.
        + count_sheep: enter
        - count_sheep: exit. took 0.00 ms.
      count_barnyard_animals: total barnyard animals: 17
    - count_barnyard_animals: exit. took 0.18 ms.
```
