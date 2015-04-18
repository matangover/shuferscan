import tesserpy
import scipy.ndimage
import os.path
from collections import namedtuple

shuf_path = "/Users/matan/Documents/code/receipts/receipt_training/shuf"
tessdata_path = "/usr/local/Cellar/tesseract/HEAD/share"
test_image = os.path.join(shuf_path, "shuf.shuf.exp0.png")

Rectangle = namedtuple("Rectangle", "left, top, right, bottom")
items_table_box = Rectangle(0, 0, 2000, 2000)
price_column_box = Rectangle(435, 168, 747, 3039)

def read_receipt(image_filename):
    tesseract = tesserpy.Tesseract(tessdata_path, language="shuf")
    image = scipy.ndimage.imread(image_filename)
    tesseract.set_image(image)
    #tesseract.orientation()
    #b = tesseract.get_utf8_bytes()
    #print(b.decode('utf-8', 'replace'))
    # tesseract.render_text2()
    #print("reading")
    text = tesseract.get_utf8_text() # needed for iterators
    words = tesseract.words()
    #print("yosi")
    #for i, word in enumerate(words):
    #    print(i)
    #    if word_in_column(word.bounding_box, price_column_box):
    #        print(word.text)
    prices = [word for word in words if word_in_column(word.bounding_box, price_column_box)]
    #print("yosi2")
    print([price.text.encode('utf8') for price in prices])

def word_in_column(word, column):
    return word.left >= column.left and word.right <= column.right \
        and word.top >= column.top and word.bottom <= column.bottom

if __name__ == "__main__":
    print(read_receipt(test_image))
