### Stylys ###

__version__ = '1.0.0'

# Reset the style
reset = '\u001b[0m'

# Styling like bold, italic, etc.
class style:
    def sgr(sgr: str or int or list):
        if type(sgr) == str or int:
            return f'\u001b[{str(sgr)}m'
        elif type(sgr) == list:
            return '\u001b[' + ';'.join(str(code) for code in sgr) + 'm'

    reset = sgr(0)
    bold = sgr(1)
    italic = sgr(3)
    line = sgr(4)
    strike = sgr(9)
    
# Foreground colors
class fg:
    def rgb(r: int, g: int, b: int):
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        return f'\u001b[38;2;{r};{g};{b}m'
    
    red = rgb(255, 0, 0)
    orange = rgb(255, 130, 0)
    yellow = rgb(255, 210, 0)
    green = rgb(0, 255, 0)
    cyan = rgb(0, 255, 255)
    blue = rgb(0, 0, 255)
    magenta = rgb(255, 0, 255)
    gray = rgb(125, 125, 125)
    black = rgb(0, 0, 0)
    white = rgb(255, 255, 255)

# Background Colors
class bg:
    def rgb(r: int, g: int, b: int):
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        return f'\u001b[48;2;{r};{g};{b}m'
    
    red = rgb(255, 0, 0)
    orange = rgb(255, 130, 0)
    yellow = rgb(255, 210, 0)
    green = rgb(0, 255, 0)
    cyan = rgb(0, 255, 255)
    blue = rgb(0, 0, 255)
    magenta = rgb(255, 0, 255)
    gray = rgb(125, 125, 125)
    black = rgb(0, 0, 0)
    white = rgb(255, 255, 255)