# Important
in start file put: "cli.init()"\
to update&render put "cli.update()" and "c.draw()"\
to clear "cli.clear()"
# Example code:
```
import cli
import vec
cli.init()
pos = vec.Vec2d(0)
vec = vec.Vec2d(0.5, 0.3)
vec.norm()

while True:
  cli.clear()
  cli.rect(pos.x, pos.y, 0, 0, '@', (255, 0, 0), (0, 0, 0))
  pos += vec
  if pos.x >= cli.size[0] or pos.x <= 0:
    vec.x *= -1
  if pos.y >= cli.size[1] or pos.y <= 0:
    vec.y *= -1
  cli.update()
  cli.draw()
```
# Vectors
## `Vec2d` Class
Represents a 2-dimensional vector with x and y components.
### `__init__(self, x: int, y: int = None)`
Constructor for Vec2d class.
#### Parameters
- `x` (int): The x component of the vector.
- `y` (int, optional): The y component of the vector. If not provided, it is set equal to x.
### Arithmetic Operations
Vec2d supports basic arithmetic operations with other Vec2d instances, integers, and floats.
- `__sub__(self, other: Union[int, float, 'Vec2d'])`: Subtracts `other` from the vector and returns a new Vec2d.
- `__add__(self, other: Union[int, float, 'Vec2d'])`: Adds `other` to the vector and returns a new Vec2d.
- `__truediv__(self, other: Union[int, float, 'Vec2d'])`: Divides the vector by `other` and returns a new Vec2d.
- `__mul__(self, other: Union[int, float, 'Vec2d'])`: Multiplies the vector by `other` and returns a new Vec2d.
### `__eq__(self, other: 'Vec2d')`
Checks for equality between two Vec2d instances.
#### Parameters
- `other` (`Vec2d`): Another Vec2d instance to compare to.
#### Returns
- `bool`: True if both vectors have the same components, False otherwise.
### `mag(self)`
Calculates the magnitude of the vector.
#### Returns
- `float`: The magnitude of the vector.
### `from_list(cls, pos: Iterable)`
Class method to create a Vec2d instance from a list or tuple.
#### Parameters
- `pos` (Iterable): An iterable with two numeric items to be used as x and y components.
#### Returns
- `Vec2d`: A new Vec2d instance.
### `norm(self)`
Normalizes the vector to have a magnitude of 1, modifying it in-place.
## `dist(vec1: Vec2d, vec2: Vec2d)`
Function to calculate the Euclidean distance between two Vec2d instances.
#### Parameters
- `vec1` (`Vec2d`): The first vector.
- `vec2` (`Vec2d`): The second vector.
#### Returns
- `float`: The distance between vec1 and vec2.
# Rendering(wuah)
file "cli.py"\
rect(x, y, w, h, fg, bg)
## Functions Overview
### `rect(x, y, w, h, c, fg, bg)`
Draws a rectangle on the screen with specified dimensions, character, foreground color, and background color.
#### Parameters
- `x` (int): The x-coordinate of the top-left corner.
- `y` (int): The y-coordinate of the top-left corner.
- `w` (int): The width of the rectangle. Note: To draw a rectangle with actual width `w`, use `w - 1`.
- `h` (int): The height of the rectangle. Note: To draw a rectangle with actual height `h`, use `h - 1`.
- `c` (char): The character used to draw the rectangle.
- `fg` (tuple of int): The foreground color in RGB format (R, G, B).
- `bg` (tuple of int): The background color in RGB format (R, G, B).
#### Example
```python
# Draws a 1x1 red rectangle with a blue background at the top-left corner of the screen.
rect(0, 0, 0, 0, '#', (255, 0, 0), (0, 0, 255))
```
### `set_color_bg(x, y, r, g, b)`
Sets the background color of a specific screen coordinate.
#### Parameters
- `x` (int): The x-coordinate.
- `y` (int): The y-coordinate.
- `r`, `g`, `b` (int): Red, Green, and Blue color components (0-255).
### `set_char(x, y, c)`
Places a character at a specific screen coordinate.
#### Parameters
- `x` (int): The x-coordinate.
- `y` (int): The y-coordinate.
- `c` (char): The character to set.
### `blit_text(x, y, text, text_color=(255, 255, 255), back_color=None, is_vertical=False)`
Renders text on the screen at the specified location, optionally setting text and background color.
#### Parameters
- `x`, `y` (int): Starting coordinates. (what, i can use - to newline)
- `text` (str): Text to display.
- `text_color` (tuple of int, optional): RGB format text color. Defaults to white.
- `back_color` (tuple of int, optional): RGB format background color. If not specified, the background is not altered.
- `is_vertical` (bool, optional): If `True`, renders the text vertically. Defaults to `False`.
### `hide_cursor()`
Hides the cursor in the terminal.
### `show_cursor()`
Shows the cursor in the terminal.
### `clear()`
Clears the screen, resetting all characters to space and colors to defaults.
### `input_menu(width=40)`
Displays an input menu, allowing the user to input text.
#### Parameters
- `width` (int, optional): The width of the input menu. Defaults to 40.
#### Returns
- `str`: The text entered by the user.
### `draw(colored: bool = True)`
Renders the screen buffer to the terminal, with optional color support.
#### Parameters
- `colored` (bool, optional): If `True`, renders in color. If `False`, renders in monochrome. Defaults to `True`.
#### Returns
- `int`: The number of characters drawn.

# Linux&Unix support
not
