import os.path
from collections import namedtuple
import hocr

shuf_path = "/Users/matan/Documents/code/receipts/receipt_training/shuf"
tessdata_path = "/usr/local/Cellar/tesseract/HEAD/share"
test_image = os.path.join(shuf_path, "shuf.shuf.exp0.png")
hocr_filename = "/Users/matan/Documents/code/receipts/receipt_training/shuf/output2.hocr.xml"
hocr_filename = "/Users/matan/Documents/code/receipts/shuferscan/training/merged/output2.hocr.xml"

Rectangle = namedtuple("Rectangle", "left, top, right, bottom")
items_table_box = Rectangle(0, 0, 2000, 2000)
price_column_box = Rectangle(435, 168, 747, 3039)
title_column_box = Rectangle(740, 138, 1600, 2966)
barcode_column_box = Rectangle(1575, 148, 2255, 2960)

def read_receipt(image_filename):
    pages = hocr.parser.parse(hocr_filename)
    last_price_line = -1
    page = pages[0]
    for i, line in enumerate(page.lines):
        prices = [word for word in line.words if word_partially_in_column(word.box, price_column_box)]
        has_price = len(prices) >= 1
        if not has_price:
            continue

        print("=========Line %02d=========" % (i + 1))
        print(" ".join(price.text for price in prices))
        title_line = page.lines[last_price_line + 1]
        title_words = [word for word in title_line.words if word_in_column(word.box, title_column_box)]
        print(" ".join(word.text for word in title_words))
        last_price_line = i

def word_in_column(word, column):
    return word.left >= column.left and word.right <= column.right \
        and word.top >= column.top and word.bottom <= column.bottom

def word_partially_in_column(word, column, min_area_percent=70):
    intersecting_rect = Rectangle(
        max(word.left, column.left),
        max(word.top, column.top),
        min(word.right, column.right),
        min(word.bottom, column.bottom))

    return rect_area(intersecting_rect) / rect_area(word) >= min_area_percent / 100

def rect_area(rect):
    return (rect.bottom - rect.top) * (rect.right - rect.left)

if __name__ == "__main__":
    read_receipt(test_image)
