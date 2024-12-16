import easyocr

reader = None

def initilize_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'])
    return reader