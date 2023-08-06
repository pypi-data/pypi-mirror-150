# PyVCheck

A simple decorator to enforce strict python versioning for your code.

```python
@version(">=3.6")
def main():
    print("I'm definitely a Python 3.6+ code!")
```

```bash
$ python3.7 -V
python 3.7.6

$ python3.7 examples/py37/main.py
I'm definitely a Python 3.6+ code!
```
