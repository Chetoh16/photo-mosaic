from PIL import Image
import os
import math
import json

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

    new_image = image.crop((left,top,right,bottom))

    return new_image


def load_and_scale_source_images(path, size):
    """
    Loads images from the folder and rescaled them
    
    Args:
    path - path string for source images folder
    size - size/dimension to shrink the images
    
    Returns:
    images = directory of loaded and rescaled images

    """
    images = {}

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')

    for file_name in os.listdir(path):
        if file_name.lower().endswith(valid_extensions):

            # load original source image
            full_path = os.path.join(path, file_name)
            img = Image.open(full_path)

            # crop it to make it a square
            img = crop_image_into_squares(img)

            # rescale/shrink it
            img.thumbnail((size, size))

            # save to the directory
            images[file_name] = img

    return images


def get_avg_rgb_for_images(images):
    """
    Calculates the average RGB value for every image in the source images directory

    Args:
    images - a dictionary of (file names, PIL image objects)

    Returns:
    rgbs - A dictionary of (file names, average RGB values)

    """

    rgbs = {}

    # images is a dictionary: {"photo.jpg": <ImageObject>}
    # iterate through it
    for file_name, img in images.items():
        
        # convert an image into its 2-D pixel matrix
        matrix = get_pixel_matrix(img)

        # get the average rgb values for that matrix
        avg_rgb = get_avg_rgb(matrix)

        # add it to the dictionary
        rgbs[file_name] = avg_rgb
    
    return rgbs


def prepare_source_images(source_path, output_path):
    """
    Crops source images to turn them into a square and saves them in a directory.
    This is useful as it would take too long to crop AND rescale 1000 images at each run.
    Only need to run it once at the beginning (if the pictures are not already square).

    Args:
    source_path - directory path of the original not-square images
    output_path - directory path of where the new square images will be saved

    """

    # create the new folder if it doesn't exist yet
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    processed_count = 0
    
    # loop through the files one by one
    for file_name in os.listdir(source_path):
        if file_name.lower().endswith(valid_extensions):
            src_path = os.path.join(source_path, file_name)
            out_path = os.path.join(output_path, file_name)
            
            try:
                with Image.open(src_path) as img:
                    
                    # crop it to make it a square
                    square_img = crop_image_into_squares(img)
                    
                    # save the new square image to the new directory
                    square_img.save(out_path)

                    processed_count += 1
                    
            except Exception as e:
                print(f"skip  {file_name}: {e}")
                
def pythagoras_nearest_rgb(target_rgb, source_images_mean_rgbs):
    """
    Finds the source image with the closest rgb value to the target section.

    Args:
    target_rgb - the average rgb value of the target section
    source_images_mean_rgbs - a dictionary of source (filenames, the mean RGB value of that file)

    Returns:
    best_match - the filename of the closest matching source image

    """


    # loops through filenames to return the one with the lowest color distance score
    # min() compares all distance numbers and returns the winning filename
    best_match = min(

        # list of filenames to choose from
        source_images_mean_rgbs.keys(),  
        
        # lambda filename is a helper function
        # takes a filename, looks up its RGB, and calculates distance to target
        key=lambda filename: pythagoras_colour_difference(target_rgb, source_images_mean_rgbs[filename])
    )

    # this is equivalent to the code above
    # best_match_name = None
    # best_match_color_difference = None
    # for path, source_rgb in source_images_mean_rgbs.iteritems():
    #     color_difference = pythagoras_colour_difference(target_rgb, source_rgb)
    #     if best_match_color_difference is None or color_difference < best_match_color_difference:
    #         best_match_name = path
    #         best_match_color_difference = color_difference

    return best_match
    

def pythagoras_colour_difference(p1, p2):
    """
    Calculates 3D distance between two RGB tuples / points.

    Formula -> Distance = sqrt{(R_2 - R_1)^2 + (G_2 - G_1)^2 + (B_2 - B_1)^2}

    Return:
    A  distance value
    
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)


def build_photomosaic_image(input_image_path, source_images, source_rgbs, tile_size = 50):
    """
    Builds a photomosaic image.

    Args:
    input_image_path - the path of the input image
    source_images_path - the directory path of source images
    tile_size - size of the tiles for the output picture

    Returns:
    output_image - photomosaic Image
    """

    # load input image to be mosaic-ed
    target_img = Image.open(input_image_path)

    # turn it into a 2-D pixel matrix
    target_matrix = get_pixel_matrix(target_img)

    height = len(target_matrix)
    width = len(target_matrix[0])

    output_image = Image.new("RGB", (width, height))

    for row in range(0, height, tile_size):
        for column in range(0, width, tile_size):

            # get current square and its rgb value
            current_square = get_square_from_image(target_matrix, (row,column), tile_size)
            target_rgb = get_avg_rgb(current_square)

            best_match_filename = pythagoras_nearest_rgb(target_rgb, source_rgbs)
            
            output_image.paste(source_images[best_match_filename], (column, row))
    
    return output_image

class JSONCache:
    """
    A small class that manages a cache backed
    by a JSON file on disk.
    """

    def __init__(self, cache_path):
        self.cache_path = cache_path

    def has_data(self):
        return os.path.isfile(self.cache_path)

    def write_all(self, data):
        with open(self.cache_path, 'w') as f:
            json.dump(data, f)

    def read_all(self):
        with open(self.cache_path) as f:
            return json.load(f)
