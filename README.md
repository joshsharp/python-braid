# rpython-interpreter
**Learning to build a language interpreter with RPython and RPly**

I don't really know what I'm doing but I'm interested in writing a toy language and interpreter. 
I've chosen RPython and RPly because I know Python quite well and the RPython EBNF parsing libs were confusing. 
RPly's interface is a bit higher level.

## Installing

`pip install -r requirements.txt`

## Running

`python interpreter.py`

`:a` gives you the AST of the last statement, `:e` to list environment variables, `:q` or Ctrl-C to quit. The REPL now supports multi-line input too — it'll just keep appending code and trying to interpret it until it's valid (eg. you closed the block or whatever), or you break it ;)

## Status

Basic arithmetic, floats, integers, booleans, and strings, variable assignment, if expressions, and a print() function.

The result of the last statement is stored in `it`, so you can do: 

```
>>> 5 + 5
= 10
>>> a = it
= 10
print(a)
= 10
```

Other stuff:

```
>>> 5 == 5
= true
>>> 5 != 5
= false
>>> a = 5
= 5
>>> print(a)
5
>>> print(a + 25)
30
>>> "hi" + 'hi'
= hihi
>>> "hi" * 5 - 1
= hihihihih
>>> if false: print("no") else: print("yes") end
yes
>>> a = (if true: 1 else: 5 end)
= 1
```

```
a = 50
if a == 50:
  print("doing stuff")
else:
  print("not this though")
end

>>> 5 >= 6
= false
```
```
>>> a = if true: 5 end
= 5
>>> :a
Program(BinaryOp(Variable('a'), If(Boolean(True))Then(Integer(5))Else(None)))
```

```
>>> [5, 6, ["hi", 7.0]]
= [5, 6, [hi, 7.0]]
```

## Compiling

You will need pypy so you can use RPython's compiler. Then, like so:

`python path/to/rpython/bin/rpython target.py`

This will provide a `target-c` binary which you can use as a compiled substitute for `interpreter.py`.

## Goals

A Turing-complete language with lexer, parser, bytecode compiler, VM, and JIT. 
A VM that compiles to a binary (thanks to RPython) which can run scripts interactively via REPL or passed in by filename.

## Status updates

Obviously you can read the commits but I'm also documenting my progress [on Littlelogs](http://littlelogs.co/josh/), or more specifically [posts tagged with #interpreter](http://littlelogs.co/josh/tag/interpreter/)
