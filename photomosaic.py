from PIL import Image
input_image = Image.open("assets/alex-ege-pics/SS853344.JPG")

#print(input_image.format, input_image.size, input_image.mode)

# to turn blue
# r, g, b = im.split()
# im = Image.merge("RGB", (b, g, r))

def get_pixel_matrix(image):

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
    



def get_average_colour_value(self, image):
    pass

def pixelate_image(self, iamge):
    pass

def crop_images_into_squares(self, images):
    pass

def build_mosaic_image(self, images):
    pass




pixel_matrix = get_pixel_matrix(input_image)


#input_image.show()




