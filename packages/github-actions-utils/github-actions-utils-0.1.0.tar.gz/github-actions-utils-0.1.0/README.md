# Github Actions Utils

### Log Utils
#### github group decorator
```python
from github_actions_utils.log_utils import github_group

@github_group("foo")
def foo():
    code
```
Will produce in github action log
```log
▸ foo
```
You can use the function parameters as input like:
```python
@github_group("Running $cmd")
def run(cmd):
    code
```
When your code calls the `run` function will print user the value from `cmd` parameter:
```python
run("nice command")
```
```log
▸ Running nice command
```
Even if the value is an object and you want a value from the object attribute:
```python
@github_group("Hello $(person.name)")
def hello(person):
    code
```
```python
p = Person(name="Heitor")
hello(p)
```
```log
▸ Hello Heitor
```