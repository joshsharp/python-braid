# rpython-interpreter
**Learning to build a language interpreter with RPython and Rply**

I don't really know what I'm doing but I'm interested in writing a toy language and interpreter. 
I've chosen RPython and RPly because I know Python quite well and the RPython EBNF parsing libs were confusing. 
RPly's interface is a bit higher level.

## Installing

`pip install -r requirements.txt`

## Running

`python interpreter.py`

## Status

Basic arithmetic, variable assignment, and a print() function.

```
>>> 5 + 5
= 10
>>> a = 5
= 5
>>> print(a)
5
>>> print(a + 25)
30
```
