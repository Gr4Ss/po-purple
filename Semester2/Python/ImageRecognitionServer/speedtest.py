import Image_2
import time

for i in range(0,30):
    start = time.time()
    im = Image_2.load_image()
    c1 = Image_2.fast_check_column(5,im)
    c2 = Image_2.fast_check_column(10,im)
    r1 = Image_2.fast_check_row(5,im)
    r2 = Image_2.fast_check_row(10,im)
    end = time.time()
    print end-start
