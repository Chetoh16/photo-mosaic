from PIL import Image
input_image = Image.open("assets/alex-ege-pics/SS853344.JPG")

#print(input_image.format, input_image.size, input_image.mode)

# to turn blue
# r, g, b = im.split()
# im = Image.merge("RGB", (b, g, r))

def get_pixel_matrix(image):
    """
    Returns a 2-D pixel matrix of the input image

    Args:
    image - PIL image object

    Returns:
    pixel_matrix - A 2-D pixel matrix 

    """

    width = image.width

    # list of all pixels in the picture
    pixels = list(image.get_flattened_data())

    # turn the pixel list into a 2d array
    pixel_matrix = [pixels[i:i+width] for i in range(0, len(pixels), width)]

    # range(0, len(pixels), width)
    # 0 - start point
    # len(pixels) - end point
    # width - increment value for each_turn
    

    # this is equivalent to the code above (both are O(N))
    # i = 0

    # keep looping until you get to the end of the pixel list
    # while i <  len(pixels):

    #     i_: i + width means take a slice from the current position up to the width (end) of one row
    #     row = pixels[i : i + width]
        
    #     add_row_to_matrix
    #     pixel_matrix.append(row)

    #     move index forward by the width to get to the next row
    #     i += width
    
    return pixel_matrix
    
def get_square_from_image(pixels, corner, size):
    """
    Returns a square of the 2-D pixel matrix of the input image

    Args:
    pixels - 2-D pixel matrix of the input image
    corner - top left corner of the sub-section/square, tuple containing coordinates(row, column)
    size - size of each square

    Returns:
    square - A 2-D pixel matrix of the sub-section/square of original matrix

    """
    
    # calculate where the square ends vertically and horizontally
    # corner is a tuple (row,column)
    row_start, col_start = corner
    row_end, col_end = row_start + size, col_start + size

    # take a slice of all the rows needed
    square_rows = pixels[row_start:row_end]

    # 2-D pixel matrix of the square
    square = []

    # the (i[x:y]) format takes a slice from x to y 
    for row in square_rows:
        square.append(row[col_start:col_end])
    
    return square


def avg_rgb(pixels):
    r_total = 0
    g_total = 0
    b_total = 0
    
    # total would be amount of rows * the width of a row
    # len(pixels) is the height (number of rows)
    # len(pixels[0]) is the width (number of pixels in the first row)
    total_pixels = len(pixels) * len(pixels[0])

    #    pixel_matrix = [pixels[i:i+width] for i in range(0, len(pixels), width)]

    for row in pixels:
        for i in row:
            r_total += i[0] # first index which red
            g_total += i[1]
            b_total += i[2]
    
    avg_rgb = (r_total / total_pixels, g_total / total_pixels, b_total / total_pixels)
    
    return avg_rgb


    

def pixelate_image(self, iamge):
    pass


def build_mosaic_image(self, images):
    pass




pixel_matrix = get_pixel_matrix(input_image)


#input_image.show()




