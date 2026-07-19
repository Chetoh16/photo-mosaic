from photomosaic import *

if __name__ == "__main__":

    # image chosen to be mosaic-ed
    input_image_path = "assets/alex-ege-pics/SS853344.JPG"

    # directory of source images (should be squares)
    source_images_dir_path = "assets/square-source-pics"

    # size of each square tile block in pixels
    tile_size = 50  

    mosaic_image = build_photomosaic_image(input_image_path, source_images_dir_path, tile_size)

    mosaic_image.show()
