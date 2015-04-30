import os.path
from collections import namedtuple
import hocr

shuf_path = "/Users/matan/Documents/code/receipts/receipt_training/shuf"
tessdata_path = "/usr/local/Cellar/tesseract/HEAD/share"
test_image = os.path.join(shuf_path, "shuf.shuf.exp0.png")
hocr_filename = "/Users/matan/Documents/code/receipts/receipt_training/shuf/output2.hocr.xml"
hocr_filename = "/Users/matan/Documents/code/receipts/shufscan/training/merged/output2.hocr.xml"

Rectangle = namedtuple("Rectangle", "left, top, right, bottom")
items_table_box = Rectangle(0, 0, 2000, 2000)
price_column_box = Rectangle(435, 168, 747, 3039)
title_column_box = Rectangle(740, 138, 1600, 2966)

def read_receipt(image_filename):
    pages = hocr.parser.parse(hocr_filename)
    for i, line in enumerate(pages[0].lines):
        prices = [word for word in line.words if word_in_column(word.box, price_column_box)]
        has_price = len(prices) >= 1
        if not has_price:
            continue
        print("Line %s" % (i + 1))
        print("\t" + " ".join(price.text for price in prices))
        title_words = [word for word in line.words if word_in_column(word.box, title_column_box)]
        print("\t" + " ".join(word.text for word in title_words))

def word_in_column(word, column):
    return word.left >= column.left and word.right <= column.right \
        and word.top >= column.top and word.bottom <= column.bottom

if __name__ == "__main__":
    print(read_receipt(test_image))
