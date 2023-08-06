# pywebcanvas
pywebcanvas is a library that allows users to interact with the HTML Canvas with 100% Python + HTML.

## Getting Started
Just add the following to an html file and you are ready to go!

Between the head tags, add pyscript and pywebcanvas:
```html
<link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />                                                         
<script defer src="https://pyscript.net/alpha/pyscript.js"></script>
<py-env>
  - pywebcanvas
</py-env>
```

In the body, you can customize the following:
```python
<py-script>
import pywebcanvas as pwc                                                                                                            

canvas = pwc.Canvas(800, 600)                                                                                                        
canvas.background.fill("blue")                                                                                                       
text = pwc.Text(text="Hello World from pywebcanvas!", x=100, y=100, size=25, color="yellow")                                         
canvas.render(text)
</py-script>
```

## Documentation
Checkout the following to learn how to use this project:
- [pywebcanvas](https://gitlab.com/imbev/pywebcanvas)
- [pyscript](https://github.com/pyscript/pyscript)
- [pyodide](https://readthedocs.org/projects/pyodide/downloads/pdf/latest/)
- [python](https://docs.python.org/3/)
- [html](https://developer.mozilla.org/en-US/docs/Web/HTML)

## Credits
This project is made possible by the developers of pyscript, pyodide, and many others.
Licensed under [LGPL-3.0-or-later](https://gitlab.com/imbev/pywebcanvas/-/blob/master/LICENSE.md)
Copyright (C) 2022 Isaac Beverly
