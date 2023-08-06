# nscmd

A terminal user interface (TUI) Python library utilizing inheritance to create namespaces for command execution. The project stemmed from a large refactoring of the cmd library, and eventually led to building an entirely separate library for the sake of design and code cleanliness.

This library currently is only targeted at GNU/Linux platforms due to its use of the readline library for several major features.

## Features

- Namespaces
- Built-in help via docstrings
- Command history
- Tab complete
- Clear terminal
- Multi-file interpreter

# Example

In a file called `bar.py`:

```python
from foo import FooInterpreter

class BarInterpreter(FooInterpreter):
    name        = 'bar'

    def do_helloworld(self, args):
        return "Hello, bar!"
```

In a file called `foo.py`:

```python
import nscmd

class FooInterpreter(nscmd.SubInterpreter):
    name        = 'foo'

    def do_helloworld(self, args):
        """prints Hello, foo!"""
        return "Hello, foo!"

if __name__ == "__main__":

    # JIT imports allow for multi-file interpreters
    from bar import BarInterpreter

    # run commands from a list...
    cmds = ["main foo","helloworld","main foo bar helloworld"]
    m = nscmd.MainInterpreter(cmd_in=cmds)
    m.run()
    # ... and get the results in a list!
    print(nscmd.outqueue)

    # ... or use files for input and output
    m = nscmd.MainInterpreter(
        cmd_in="example_cmds.txt",
        outfile="example_output.txt"
    )
    m.run()

    # Use a string!
    cmdstr = "main foo\nhelloworld\nmain foo bar helloworld\n"
    m = nscmd.MainInterpreter(
        cmd_in=cmdstr
    )
    m.run()
    print(nscmd.outqueue)

    # or run as a standard TUI
    m = nscmd.MainInterpreter()
    m.tui()

    # no matter what method you use, you can still access
    # the output as a list. It resets on each instantiation.
    print(nscmd.outqueue)

```
