import js


logging = True

def log(message: str):
    global logging
    if logging:
        js.console.log(f"pywebcanvas: {message}")

def disable_logging(disable: bool):
    global logging 
    logging = not disable
    log(f"{logging=}")
