# slf4py
Simple Logging Facade for Python.

## How to use
```bash
# at Terminal

$ pip install slf4py
```

```python
# at example.py

from slf4py import set_logger


@set_logger
class Example:
    def hi(self):
        self.log.info("Hello World")

        
e = Example()
e.hi()
# [INFO] [2022-05-01 11:22:35,493] [example.py:9] Hello World
```