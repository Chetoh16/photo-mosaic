from PIL import Image

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


def get_avg_rgb(pixels):
    """
    Returns the average rgb value of a pixel matrix
    
    Args:
    pixels - 2-D pixel matrix of the input image

    Returns:
    avg_rgb = A 3-tuple of avg rgb value of the matrix

    """

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
    
    avg_rgb = (int(r_total / total_pixels), int(g_total / total_pixels), int(b_total / total_pixels))
    
    return avg_rgb


def pixelate_image(pixels, size=50):
    """
    Pixelates an image with mean RGB values for the squares
    
    Args:
    pixels - 2-D pixel matrix of the input images
    size - size of the squares

    Returns:
    output_pixels = A 2-D matrix of average RGB values

    """

    height = len(pixels)
    width = len(pixels[0])

    # create a new blank image matrix
    output_pixels = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    for row in range(0, height, size):
        for column in range(0, width, size):
            
            # extract the current square block and get its average colour
            current_square = get_square_from_image(pixels, (row,column), size)
            square_avg_rgb = get_avg_rgb(current_square)

            # put the average colour into the new output matrix
            for square_row in range(row, min(row + size, height)):
                for square_column in range(column, min(column + size, width)):
                    output_pixels[square_row][square_column] = square_avg_rgb
    
    return output_pixels    


def crop_image_into_squares(image):
    """
    Crops an image to turn it into a square by cropping it from the centre
    
    Args:
    image - Image object
    
    Returns:
    new_image = Square Image object

    """

    #crop from the exact centre

    height = image.height
    width = image.width

    # take the smallest side to turn into a square
    # i.e. from (1280, 800) to (800,800)
    new_size = min(width,height)

    # calculate how much extra space needs to be split evenly on both sides
    left = (width - new_size) // 2
    top = (height - new_size) // 2
    
    # calculate the ending bounds based on the centre starting points
    right = left + new_size
    bottom = top + new_size

    new_image = image.crop(left,top,right,bottom)

    return new_image


def build_mosaic_image(self, images):
    pass


input_image = Image.open("assets/alex-ege-pics/SS853344.JPG")
input_image_width = input_image.width
input_image_height = input_image.height

pixel_matrix = get_pixel_matrix(input_image)

# 2-D matrix for the pixelated image with average RGB values      
pixelated_input_image_matrix = pixelate_image(pixel_matrix)

# output image
output_image = Image.new("RGB", (input_image_width, input_image_height))

# convert 2-D matrix into 1-D in order to put that pixel value data into the image
flat_pixels = [pixel for row in pixelated_input_image_matrix for pixel in row]
output_image.putdata(flat_pixels)

output_image.show()




