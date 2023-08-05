# Better-Turtle

## Installation
```
pip install BetterTurtle
```

## Updating
```
pip install --force-reinstall BetterTurtle
```

## Basic usage
```python
from BetterTurtle import BetterTurtle
screen = BetterTurtle()
t = screen.get_turtle()

for i in range(10):
    t.forward(100)
    t.right(90)

screen.not_exit()
```

The `BetterTurtle` class can get additional args. Theese are ` title: str="BetterTurtle", geometry: str="500x500", active_control: bool=True`.
  * `title` is a string that will set be set as the title of the window
  * `geometry` is a string that will set the initial size of the window
  * `active_control` is a bool that manages if the buttons work or not. This can be changed after creating the object