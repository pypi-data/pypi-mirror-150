# Templo

A generic template language.

## Installation

Run the following command to install:

```python
pip install templo
```

## Usage

```python
from templo import template

# Generate a render funtion
render = template("foo {{ 2 + 3 }} bar")
# returns 'foo 5 bar'
render()

# Generate a render function and pass a dictionary
d = {"name": "Diana"}
render = template("Hello, {{ name or 'World' }}!")
# returns 'Hello, World!'
render()
# returns 'Hello, Diana!'
render(d)

# Generate final text
# returns 'Hello, simple world!'
template("Hello,{% if answer == 42 %} simple {% else %} cruel {% endif %}world!", {'answer': 42})
# returns 'Hello, cruel world!'
template("Hello,{% if answer == 42 %} simple {% else %} cruel {% endif %}world!", {'answer': 73})
```
