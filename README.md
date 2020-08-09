Wack is a personal project to provide a simple [click](https://github.com/pallets/click) cli tool. Wack gives the user the ability to make files quickly and the ability to write simple and quick cli commands.

Install:
```
pip install wack
```

Now `wack` will be added to your terminal commands. Typing `wack` will give you:
```
Usage: wack [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init
  install
  make
```

Setup:
```
wack init
```

This will make a wack.py file in the directory you're in. My recommendation is to do this in the root dir. It will look like the below:
```
from wack import command
from wack import echo


@command()
def hello_world():
    echo("hello world")
```




#### TODO
* install dotenv
* pre-commit
