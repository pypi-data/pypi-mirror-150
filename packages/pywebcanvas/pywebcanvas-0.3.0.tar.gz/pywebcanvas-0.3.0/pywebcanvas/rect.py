import js
from colour import Color
import pywebcanvas as pwc


class Rect:
    def __init__(self, x, y, width, height, color="black", type_="fill"):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.color = color
        self.type_ = type_
    
    def render(self, canvas):
        pwc.log(f"Render Rect {self} at x {self.x}, y {self.y}, width {self.width}, height {self.height}, color {self.color}, type_ {self.type_}")

        ctx = canvas.ctx()

        hex_color = Color(self.color).hex 
        ctx.fillStyle = hex_color

        args = (self.x, self.y, self.width, self.height)

        if self.type_ == "fill":
            ctx.fillRect(*args)
        elif self.type_ == "stroke":
            ctx.strokeRect(*args)
        elif self.type_ == "clear":
            ctx.clearRect(*args)
