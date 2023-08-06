# slap.core.cli

Extension of [`argparse`][0] to provide fast and customizable argument parsing.

  [0]: https://docs.python.org/3/library/argparse.html

## Features

* Minimal API; interact mostly `argparse`
* Fast; because `argparse` is fast
* Completion; built-in support

## Usage

```py
import argparse
from typing import Any, Optional

from slap.core.cli import CliApp, Command
from slap.core.cli.completion import CompletionCommand


class HelloCommand(Command):
    """ say hello to someone """

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("name")

    def execute(self, args: Any) -> Optional[int]:
        print(f"Hello, {args.name}!")


app = CliApp("minimal", "0.1.0")
app.add_command("hello", HelloCommand())
app.add_command("completion", CompletionCommand())
app.run()
```

Gives you the following CLI:

```
$ python examples/minimal.py
usage: minimal [-h] [-v] [--version] [{hello,completion}] ...

positional arguments:
  {hello,completion}  the subcommand to execute
  ...                 arguments for the subcommand

options:
  -h, --help          show this help message and exit
  -v, --verbose       increase the verbosity level
  --version           show program's version number and exit

subcommands:
  hello               say hello to someone
  completion          completion backend for bash
```

> __On Completion__
>
>
> You can run `python examples/minimal.py completion --bash` to get the code that should be run in your
> shell to enable completion features. However, you will need to make command available as a first-order
> command in your shell for completion to work (e.g. `minimal` instead of `python examples/minimal.py`).

## Compatibility

Requires Python 3.6 or higher.
